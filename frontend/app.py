import base64
import hashlib
import hmac
import os

import requests
import streamlit as st


def make_rowid(primaryKey: str, secret_key: str = os.environ["HASH_KEY"]) -> str:
    message = primaryKey.encode("utf-8")
    key = secret_key.encode("utf-8")

    digest = hmac.new(key, message, hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def set_vars() -> None:
    st.session_state["user"] = st.session_state.get("user", None)
    if st.session_state.user is not None:
        st.session_state.shopping_lists = requests.get(
            f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists/list", timeout=300
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
            st.session_state.user = user
        st.rerun()


@st.dialog("Sign Up")
def signup() -> None:
    username = st.text_input("Username")
    email = st.text_input("Email")
    if st.button("Submit"):
        user = {"name": username, "email": email}
        new_user = requests.post(
            f"{os.environ['BACKEND_ENDPOINT']}/users", json=user, timeout=300
        ).json()
        if "detail" in new_user:
            st.error(new_user["detail"])
        else:
            st.success(f"Created user with email {new_user['email']}")
            st.session_state.user = new_user
        st.rerun()


@st.dialog("Add item")
def add_item():
    pass


@st.dialog("Make Shopping List")
def make_list():
    name = st.text_input("Shopping List Name:")
    if st.button("Submit"):
        list = {"name": name, "owner": st.session_state.user["id"]}
        new_user = requests.post(
            f"{os.environ['BACKEND_ENDPOINT']}/shoppinglists", json=list, timeout=300
        ).json()
        if "detail" in new_user:
            st.error(new_user["detail"])
        else:
            st.success(f"Created {list['name']} shopping list.")
            st.session_state.user = new_user
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


def main() -> None:
    set_vars()
    header_col1, header_col2 = st.columns([1, 1])
    with header_col1:
        st.title("Shopping List")
    with header_col2:
        st.write("")
        login_col, signup_col = st.columns([1, 1])
        with login_col:
            if st.button("Login", type="primary"):
                login()
        with signup_col:
            if st.button("Sign up", type="primary"):
                signup()
    st.divider()

    if st.session_state.user is not None:
        new_col, _, delete_col = st.columns([1, 4, 1])
        with new_col:
            if st.button("New list"):
                make_list()
        if len(st.session_state.shopping_lists):
            tabs = st.tabs([slist["name"] for slist in st.session_state.shopping_lists])
            for i, tab in enumerate(tabs):
                with delete_col:
                    if st.button("Delete list", key=f"delete_{tab}"):
                        delete_list(st.session_state.shopping_lists[i])
                with tab:
                    if st.button(
                        "+ Add item",
                        type="primary",
                        use_container_width=True,
                        key=f"item_{tab}",
                    ):
                        add_item()
                    st.write("test")


if __name__ == "__main__":
    main()
