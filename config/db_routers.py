class MarketdataRouter:
    route_app_labels = {'marketdata'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'marketdata_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return True
        return None


class PrimaryRouter:
    def db_for_read(self, model, **hints):
        return 'primary'

    def db_for_write(self, model, **hints):
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        db_set = {'primary'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # if app_label == 'marketdata':
        #     return False
        return True
