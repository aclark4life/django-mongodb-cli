def mongo_launch(launch_type=None):
    if launch_type:
        return ["mongo-launch", launch_type]
    else:
        return ["mongo-launch", "single"]


def postgres_launch():
    return [
        "/opt/homebrew/opt/postgresql@14/bin/postgres",
        "-D",
        "/opt/homebrew/var/postgresql@14",
    ]
