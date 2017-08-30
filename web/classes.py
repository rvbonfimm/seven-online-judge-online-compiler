
Class User():
	
	id = 
	username = 
	password = 
	name = 
	lastname = 
	email =
	gender = 
    date_created = 

    @property
    def is_authenticated(self):

        return True

    @property
    def is_active(self):

        return True

    @property
    def is_anonymous(self):

        return False

    def get_id(self):

        try:

            return unicode(self.id)  # python 2

        except NameError:

            return str(self.id)  # python 3