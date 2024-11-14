from app.services.CRUDuser_service import retrieving_user_service, add_user_service, change_status_account_service, \
    updating_user_service, locked_user_service, unlocked_user_service, locking_for_user_service


def retrieving_user_controller():
    return retrieving_user_service()


def add_user_controller():
    return add_user_service()


def change_status_account_controller(customer_id):
    return change_status_account_service(customer_id)


def updating_user_controller(customer_id):
    return updating_user_service(customer_id)


def locked_user_controller(customer_id):
    return locked_user_service(customer_id)


def unlocked_user_controller(customer_id):
    return unlocked_user_service(customer_id)


def locking_for_user_controller():
    return locking_for_user_service()
