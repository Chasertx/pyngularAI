from django.core.mail.backends.smtp import EmailBackend
import ssl
import certifi

#Custom email backend. 
class CustomEmailBackend(EmailBackend):
    #Overriding the open method. We want to customize how the SMTP connection is established.
    def open(self):
        #Checking if there is already a connection.
        if self.connection:
            return False
        try:
            #Create a new SMTP connection.
            #users a the configured host, port, and timeout.
            self.connection = self.connection_class(self.host, self.port, timeout=self.timeout)
            #Initiating the SMTP convo.
            self.connection.ehlo()

           
            #This checks if TLS secure connection is enabled.
            if self.use_tls:
                #Creating a custom SSL context. Using certifi.
                context = ssl.create_default_context(cafile=certifi.where())

                #REMOVE IN PRODUCTION. bypassing ssl security checks.
                #Disabling hostname checking.
                context.check_hostname = False
                #Disabling certificate verification.
                context.verify_mode = ssl.CERT_NONE  # WARNING: use only in dev!

                #Initializing the TLS encryption with the custom SSL context.
                self.connection.starttls(context=context)
                #Resending ehlo after starting the TLS
                self.connection.ehlo()

            #If username and password are provided. loging to the smtp server.
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            #Return true for successful connection.
            return True
        except Exception as e:
            print("EMAIL ERROR:", e)
            if not self.fail_silently:
                raise
