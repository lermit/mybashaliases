import re
from django.core.validators import RegexValidator

alias_re = re.compile(
  r'^[^ =]=[^ ]*|\'.*\'|".*"$')

class AliasValidator(RegexValidator):
  regex = alias_re
  message = 'Enter a valid alias'
  code = 'invalid_alias'
