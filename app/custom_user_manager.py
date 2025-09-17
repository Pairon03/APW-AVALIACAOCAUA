from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, name, cpf, rg, birth_date, 
                       address_country, address_state, address_city,
                       address_district, address_street, address_zip_code,
                       address_number, **extra_fields):
        
        if None in (email, password, name, cpf, rg, birth_date, 
                       address_country, address_state, address_city,
                       address_district, address_street, address_zip_code,
                       address_number):
            raise ValueError('Missing required fields during user creation')
        
        extra_fields.setdefault('is_active',True)
        user = self.model(email=self.normalize_email(email), 
                          name=name, cpf=cpf, rg=rg, birth_date=birth_date, 
                          address_country=address_country, 
                          address_state=address_state, 
                          address_city=address_city,
                          address_district=address_district, 
                          address_street=address_street, 
                          address_zip_code=address_zip_code,
                          address_number=address_number, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password, name, cpf, rg, birth_date, 
                       address_country, address_state, address_city,
                       address_district, address_street, address_zip_code,
                       address_number, **extra_fields):
        
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email, password, name, cpf, rg, birth_date, 
                       address_country, address_state, address_city,
                       address_district, address_street, address_zip_code,
                       address_number, **extra_fields)