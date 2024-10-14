class Provider:
    GOOGLE = "GOOGLE"
    GITHUB = "GITHUB"
    DISCORD = "DISCORD"
    NO_PROVIDER = "NO_PROVIDER"


class Role:
    RESTO_OWNER = "RESTO_OWNER"
    CUSTOMER = "CUSTOMER"

    @classmethod
    def get_roles(cls):
        return [
            (cls.RESTO_OWNER, "Restoran Owner"),
            (cls.CUSTOMER, "Customer"),
        ]
