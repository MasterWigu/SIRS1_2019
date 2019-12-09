function checkForm(form) {
  if(form.username.value == "") {
    alert("Error: Username cannot be blank!");
    form.username.focus();
    return false;
  }

  if(form.password.value != "") {
    if(form.password.value.length < 6) {
      alert("Error: Password must contain at least six characters!");
      form.password.focus();
      return false;
    }
    if(form.password.value == form.username.value) {
      alert("Error: Password must be different from Username!");
      form.password.focus();
      return false;
    }
    re = /[0-9]/;
    if(!re.test(form.password.value)) {
      alert("Error: password must contain at least one number (0-9)!");
      form.password.focus();
      return false;
    }
    re = /[a-z]/;
    if(!re.test(form.password.value)) {
      alert("Error: password must contain at least one lowercase letter (a-z)!");
      form.password.focus();
      return false;
    }
    re = /[A-Z]/;
    if(!re.test(form.password.value)) {
      alert("Error: password must contain at least one uppercase letter (A-Z)!");
      form.password.focus();
      return false;
    }
  } else {
    alert("Error: Password cannot be blank!");
    form.password.focus();
    return false;
  }

  return true;
}
