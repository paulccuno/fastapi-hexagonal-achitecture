class BaseEntity:
    def __init__(self, user_record_creation, record_creation_date, user_edit_record, record_edit_date, record_status):
        self.user_record_creation = user_record_creation
        self.record_creation_date = record_creation_date
        self.user_edit_record = user_edit_record
        self.record_edit_date = record_edit_date
        self.record_status = record_status
