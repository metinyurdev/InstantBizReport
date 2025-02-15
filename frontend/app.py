import streamlit as st
from pages.login import show_login
from pages.dashboard import show_dashboard
from pages.sales import show_sales
from pages.personals import show_personals
from pages.finance import show_finance
from pages.logout import logout

# Ana uygulama
def main():
    # Session state'i başlat
    if "token" not in st.session_state:
        st.session_state.token = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"

    # Token kontrolü
    if st.session_state.token is None:
        show_login()  # Login sayfasını göster
    else:
        if st.session_state.current_page == "dashboard":
            show_dashboard()  # Dashboard sayfasını göster
        elif st.session_state.current_page == "sales":
            show_sales()  # Sales sayfasını göster
        elif st.session_state.current_page == "personals":
            show_personals()  # Personals sayfasını göster
        elif st.session_state.current_page == "finance":
            show_finance()  # Finance sayfasını göster

if __name__ == "__main__":
    main()