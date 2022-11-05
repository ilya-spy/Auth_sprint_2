from flask import Blueprint, Flask

import api.v1.controllers as api_v1_c


def init_routes(app: Flask):
    api = Blueprint("api", __name__, url_prefix="/api")
    api_v1 = Blueprint("v1", __name__, url_prefix="/v1")

    setup_base_routes(api_v1)
    setup_oauth_routes(api_v1)

    api.register_blueprint(api_v1)
    app.register_blueprint(api)

def setup_oauth_routes(api: Blueprint):
    """Добавить OAuth эндпоинты в целевое АПИ"""

    # Регистрация путей
    api.add_url_rule(
        "/login/yandex/authorize",
        "Yandex OAuth2 login Hand-Shake",
        view_func=api_v1_c.get_oauth_controller().yandex_authorize,
        methods=[
            "POST",
        ],
    )
    api.add_url_rule(
        "/login/yandex",
        "Get Yandex OAuth2 login handle",
        view_func=api_v1_c.get_oauth_controller().yandex,
        methods=[
            "GET",
        ],
    )
    api.add_url_rule(
        "/login/google",
        "Get Google OAuth2 login dialog",
        view_func=api_v1_c.get_oauth_controller().google,
        methods=[
            "GET",
        ],
    )
    api.add_url_rule(
        "/login/facebook",
        "Get Facebook OAuth2 login dialog",
        view_func=api_v1_c.get_oauth_controller().facebook,
        methods=[
            "GET",
        ],
    )

def setup_base_routes(api_v1: Blueprint):
    api_v1.add_url_rule(
        "/ping",
        "ping",
        view_func=api_v1_c.get_health_check_controller().ping,
        methods=["GET"],
    )

    api_v1.add_url_rule(
        "/login",
        "login",
        view_func=api_v1_c.get_auth_controller().login,
        methods=[
            "POST",
        ],
    )

    api_v1.add_url_rule(
        "/user",
        "register_user",
        view_func=api_v1_c.get_auth_controller().register_user,
        methods=[
            "POST",
        ],
    )

    api_v1.add_url_rule(
        "/me/refresh_token",
        "refresh_token",
        view_func=api_v1_c.get_auth_controller().refresh_token,
        methods=[
            "PUT",
        ],
    )

    api_v1.add_url_rule(
        "/me",
        "update_current_user",
        view_func=api_v1_c.get_user_controller().update_current_user,
        methods=[
            "PUT",
        ],
    )

    api_v1.add_url_rule(
        "/me/access_history",
        "get_access_history",
        view_func=api_v1_c.get_access_history_controller().get_access_history,
        methods=["GET"],
    )

    api_v1.add_url_rule(
        "/me/logout",
        "logout",
        view_func=api_v1_c.get_auth_controller().logout,
        methods=[
            "GET",
        ],
    )

    api_v1.add_url_rule(
        "/me/logout_other_devices",
        "logout_other_devices",
        view_func=api_v1_c.get_auth_controller().logout_other_devices,
        methods=[
            "GET",
        ],
    )

    api_v1.add_url_rule(
        "/role",
        "get_roles",
        view_func=api_v1_c.get_role_controller().get_roles,
        methods=[
            "GET",
        ],
    )

    api_v1.add_url_rule(
        "/role/<role_id>",
        "get_role",
        view_func=api_v1_c.get_role_controller().get_role,
        methods=[
            "GET",
        ],
    )

    api_v1.add_url_rule(
        "/role",
        "create_role",
        view_func=api_v1_c.get_role_controller().create_role,
        methods=[
            "POST",
        ],
    )

    api_v1.add_url_rule(
        "/role/<role_id>",
        "update_role",
        view_func=api_v1_c.get_role_controller().update_role,
        methods=[
            "PUT",
        ],
    )

    api_v1.add_url_rule(
        "/role/<role_id>",
        "delete_role",
        view_func=api_v1_c.get_role_controller().delete_role,
        methods=[
            "DELETE",
        ],
    )

    api_v1.add_url_rule(
        "/user/<user_id>/role/<role_id>",
        "check_user_role",
        view_func=api_v1_c.get_user_controller().check_user_role,
        methods=[
            "GET",
        ],
    )

    api_v1.add_url_rule(
        "/user/<user_id>/role/<role_id>",
        "set_role_to_user",
        view_func=api_v1_c.get_user_controller().set_role_to_user,
        methods=[
            "POST",
        ],
    )

    api_v1.add_url_rule(
        "/user/<user_id>/role/<role_id>",
        "delete_user_role",
        view_func=api_v1_c.get_user_controller().delete_user_role,
        methods=[
            "DELETE",
        ],
    )
