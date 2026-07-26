import modal


APP_NAME = "executive-classifier-api"
MODEL_VOLUME_NAME = "executive-classifier-model"
MODEL_MOUNT_PATH = "/models"

image = (
    modal.Image.debian_slim(python_version="3.12")
    .pip_install_from_requirements("backend/requirements-modal.txt")
    .env(
        {
            "ALLOWED_ORIGINS": "https://executive-classifier.vercel.app",
        }
    )
    .add_local_python_source("app")
)
model_volume = modal.Volume.from_name(
    MODEL_VOLUME_NAME,
    create_if_missing=False,
)
app = modal.App(APP_NAME)


@app.function(
    image=image,
    gpu="T4",
    volumes={MODEL_MOUNT_PATH: model_volume},
    min_containers=0,
    max_containers=1,
    scaledown_window=60,
    timeout=2 * 60,
    startup_timeout=5 * 60,
)
@modal.concurrent(max_inputs=1)
@modal.asgi_app()
def fastapi_app():
    from app.main import app as fastapi_application

    return fastapi_application
