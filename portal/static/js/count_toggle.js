function toggleInputField(checkbox) {
  const inputField = checkbox.parentElement.parentElement.querySelector('.cell3');
  if(!checkbox.checked){
    inputField.readOnly = true;
    inputField.value = 0;
  }
  else{
    inputField.readOnly = false;
    inputField.value = 1;
  }
}
