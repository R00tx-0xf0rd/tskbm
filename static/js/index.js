function redirect()
{
console.log('clicked');
window.location='/'
}


function doFunction() {
setTimeout(redirect, 5000);
}


function process() {
if (confirm('Хотите добавить срок поверки ?')) {
  // Save it!
  console.log('Thing was saved to the database.');
} else {
  // Do nothing!
  console.log('Thing was not saved to the database.');
}
}