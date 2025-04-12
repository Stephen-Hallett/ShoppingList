import base64
import hashlib
import hmac
import os

import requests
import streamlit as st


def make_rowid(primaryKey: str, secret_key: str = os.environ["HASH_KEY"]) -> str:
    message = primaryKey.encode("utf-8").lower().strip()
    key = secret_key.encode("utf-8")

    digest = hmac.new(key, message, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def set_vars() -> None:
    if "id" in st.query_params:
        st.session_state["user"] = requests.get(f"{os.environ['BACKEND_ENDPOINT']}/users/{st.query_params.id}").json()
    else:
        st.session_state["user"] = None
    if st.session_state.user is not None:
        st.session_state.shopping_lists = requests.get(
            f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/{st.session_state.user['id']}/list", timeout=300
        ).json()


@st.dialog("Login")
def login() -> None:
    email = st.text_input("Email")
    if st.button("Submit"):
        user = requests.get(
            f"{os.environ['BACKEND_ENDPOINT']}/users/{make_rowid(email)}", timeout=300
        ).json()
        if "detail" in user:
            st.error(user["detail"])
        else:
            st.success(f"Welcome back {user['name']}")
            st.query_params.id=user["id"]
        st.rerun()


@st.dialog("Sign Up")
def signup() -> None:
    username = st.text_input("Username")
    email = st.text_input("Email")
    if st.button("Submit"):
        user = {"name": username.capitalize(), "email": email}
        new_user = requests.post(
            f"{os.environ['BACKEND_ENDPOINT']}/users", json=user, timeout=300
        ).json()
        if "detail" in new_user:
            st.error(new_user["detail"])
        else:
            st.success(f"Created user with email {new_user['email']}")
            st.query_params.id=user["id"]
        st.rerun()


@st.dialog("Add item")
def add_item(shopping_list: dict) -> None:
    new_item = st.text_input("Item").capitalize()
    item_id = make_rowid(new_item)
    if st.button("Add item"):
        _ = requests.post(
            f"{os.environ['BACKEND_ENDPOINT']}/items",
            json={"name": new_item},
            timeout=300,
        ).json()
        if item_id not in shopping_list["items"]:
            shopping_list["items"].append(item_id)
            _ = requests.put(
                f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/{shopping_list['id']}",
                json=shopping_list,
                timeout=300,
            ).json()
        else:
            st.error(f"{new_item} is already in the {shopping_list['name']} list.")
        st.rerun()


@st.dialog("Make Shopping List")
def make_list() -> None:
    name = st.text_input("Shopping List Name:")
    if st.button("Submit"):
        slist = {"name": name.capitalize(), "owner": st.session_state.user["id"]}
        new_list = requests.post(
            f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists", json=slist, timeout=300
        ).json()
        if "detail" in new_list:
            st.error(new_list["detail"])
        else:
            st.success(f"Created {list['name']} shopping list.")
        st.rerun()


@st.dialog("Delete list")
def delete_list(tab: str) -> None:
    delete = st.toggle(f'Delete "{tab["name"]}" list?')
    if delete:  # NOQA
        if st.button("Delete", type="primary"):
            response = requests.delete(
                f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/{tab['id']}",
                timeout=300,
            ).json()
            if "detail" in response:
                st.error(response["detail"])
            else:
                st.success(f"Deleted {tab['name']} shopping list.")
            st.rerun()

@st.dialog("Users")
def manage_users(shopping_list: dict) -> None:
    new_user = st.text_input("User Email").capitalize()
    if st.button("Invite User", type="primary"):
        invited_user = requests.get(f"{os.environ['BACKEND_ENDPOINT']}/users/{make_rowid(new_user)}").json()
        if "detail" in invited_user:
            st.error(f"There is no user with the email {new_user}")
        else:
            _ = requests.put(
                f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/{shopping_list['id']}/members/invite",
                json={"email": new_user},
                timeout=300,
            ).json()
        st.rerun()
    st.write("Remove users")
    invited_users = [requests.get(f"{os.environ['BACKEND_ENDPOINT']}/users/{user_id}").json() for user_id in shopping_list["members"]]
    selected_user = st.pills("Users", [user["name"] for user in invited_users])
    if selected_user is not None:
        if st.button(f"Remove {selected_user} from {shopping_list['name']} list?", type="primary"):
            _ = requests.delete(
                f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/{shopping_list['id']}/members/delete",
                json={"email": [user for user in invited_users if user["name"] == selected_user][0]["email"]},
                timeout=300,
            ).json()
            st.rerun()



def delete_item(shopping_list: dict, item: str) -> None:
        _ = requests.delete(
            f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/{shopping_list['id']}/items/delete",
            json={"item": item},
            timeout=300,
        ).json()
        st.rerun()

def app() -> None:
    header_col1, _, header_col2 = st.columns([2, 3, 1])
    with header_col1:
        st.title("Shopping List")
    with header_col2:
        st.write("")
        login_col, signup_col = st.columns([1, 1])
        with login_col:
            if st.button("Login", type="primary", use_container_width=True):
                login()
        with signup_col:
            if st.button("Sign up", type="primary", use_container_width=True):
                signup()
    st.divider()

    if st.session_state.user is not None:
        message_col, _, new_col = st.columns([2, 3, 1])
        with new_col:
            if st.button("New list", use_container_width=True):
                make_list()
        with message_col:
            st.markdown(f"### 👋 Hello, {st.session_state.user['name']}")
            st.write("")
        if len(st.session_state.shopping_lists):
            tabs = st.tabs([slist["name"] for slist in st.session_state.shopping_lists])
            for i, tab in enumerate(tabs):
                with tab:
                    item_col, invite_col, delete_col = st.columns([4, 1, 1])
                    with invite_col:
                        if st.button(
                            "Users", key=f"invite_{tab}", use_container_width=True
                        ):
                            manage_users(st.session_state.shopping_lists[i])
                    with delete_col:
                        if st.button(
                            "Delete List", key=f"delete_{tab}", use_container_width=True
                        ):
                            delete_list(st.session_state.shopping_lists[i])
                    with item_col:
                        if st.button(
                            ":material/add_circle: Add item",
                            type="primary",
                            use_container_width=True,
                            key=f"item_{tab}",
                        ):
                            add_item(st.session_state.shopping_lists[i])

                    for item_id in st.session_state.shopping_lists[i]["items"]:
                        with st.container(border=True):
                            info, button = st.columns([5, 1])
                            with info:
                                item_name = requests.get(
                                    f"{os.environ['BACKEND_ENDPOINT']}/items/{item_id}"
                                ).json()["name"]
                                st.markdown(f"**{item_name}**")
                            with button:
                                if st.button(
                                    ":material/delete: Delete",
                                    use_container_width=True,
                                    type="primary",
                                    key=f"delete_{item_id}"
                                ):
                                    delete_item(st.session_state.shopping_lists[i], item_name)


def main() -> None:
    set_vars()
    app()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Shopping Lists", layout="wide", page_icon=":material/shopping_cart:"
    )
    main()
