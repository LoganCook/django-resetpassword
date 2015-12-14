from ldap3 import Server, Connection, MODIFY_REPLACE

def build_password(passwd):
    quoted_passwd = "\"%s\"" % passwd
    #accept all unicode
    return quoted_passwd.encode("utf-16-le")

class ErsaAD:
  def __init__(self, server, bind_domain, bind_user, bind_pass, base_dn):
    server = Server(server, port = 636, use_ssl = True)
    self.conn = Connection(server, "%s\%s" % (bind_domain, bind_user), bind_pass, auto_bind=True)
    self.ad_base_dn = base_dn

  #return a list
  def get_user_by_email(self, email):
    email_filter = "(&(objectclass=person)(mail=%s))" % email
    self.conn.search(self.ad_base_dn, email_filter)
    return self.conn.entries

  # return True or False
  def reset_password(self, account_dn, password):
    ad_pwd = build_password(password)
    return self.conn.modify(account_dn, {'unicodePwd': [(MODIFY_REPLACE, [ad_pwd])]})
