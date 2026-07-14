import streamlit_authenticator as stauth


names=[
"Vimal"
]

usernames=[
"vimal"
]


passwords=[
"password123"
]


hashed_passwords = (
    stauth.Hasher(passwords)
    .generate()
)


authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "cookie",
    "signature"
)


def login():

    name,authentication_status,username = (
        authenticator.login()
    )


    return authentication_status