const cookies = document.cookie.split(';');
let myCookie = [];
let printCookie ='{'
for (let i = 0; i < cookies.length; i++) {
  const cookie = cookies[i].trim();
  if (cookie.startsWith('WC_AUTHENTICATION_') || cookie.startsWith('WC_USERACTIVITY_') ) {
    let separatorIndex  = cookie.indexOf("=")
    let firstPart = cookie.substring(0, separatorIndex);
    let secondPart = cookie.substring(separatorIndex + 1);
    printCookie= printCookie + '"' + firstPart + '": '
    printCookie= printCookie + '"' + secondPart + '",\n'
  }
}
printCookie = printCookie.slice(0, -2) + '}'
console.log(printCookie)