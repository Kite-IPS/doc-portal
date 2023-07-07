//pdf converting function
function generatePDF() {
    const element = document.getElementById('invoice');
    const opt = {
      margin: 0.5,
      filename: 'document.pdf',
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 1 },
      jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
    };
  
  
    html2pdf().set(opt).from(element).toPdf().output('dataurlnewwindow'); 
}
  
    
  