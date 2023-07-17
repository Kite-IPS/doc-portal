function toggleInputField(checkbox) {
  console.log(checkbox);
  const inputField = checkbox.closest('tr').querySelector('.input-field');
  inputField.disabled = !checkbox.checked;
}
