from uuid import UUID, uuid4

from fastapi import Request, Response


WORKSPACE_COOKIE = "lumen_workspace_id"


def get_workspace_id(request: Request, response: Response) -> str:
    workspace_id = request.cookies.get(WORKSPACE_COOKIE)

    try:
        UUID(workspace_id or "")
    except ValueError:
        workspace_id = str(uuid4())
        response.set_cookie(
            key=WORKSPACE_COOKIE,
            value=workspace_id,
            httponly=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 365,
        )

    return workspace_id