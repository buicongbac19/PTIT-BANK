from app.services.CRUDaccount_service import retrieving_account_service, CreateAcc_service, LockedAcc_service, \
    EditingAcc_service, UnlockedAcc_service, SearchAcc_service


def retrieving_account_controller():
    return retrieving_account_service()


def CreateAcc():
    return CreateAcc_service()


def EditingAcc(account_id):
    return EditingAcc_service()


def LockedAcc(account_id):
    return LockedAcc_service(account_id)


def UnlockedAcc(account_id):
    return UnlockedAcc_service(account_id)


def SearchAcc():
    return SearchAcc_service()
