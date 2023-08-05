const r = document.querySelector(':root');
var cc = 1;
function changeMode() {
    if (cc == 0) {
      cc = 1;
    } else {
      cc = 0;
    }

      if(cc == 0) {
        r.style.setProperty('--main-color-nav', 'black');
        r.style.setProperty('--text-color-nav', '#ffffff');
        r.style.setProperty('--secondary-color-nav', '#76abff');

        r.style.setProperty('--main-color', '#333333');
        r.style.setProperty('--text-color', '#ffffff');
        r.style.setProperty('--secondary-color', '#76abff');
        mode.innerHTML = "Light-Mode";
      } else if (cc == 1) {
        r.style.setProperty('--main-color-nav', '#333333');
        r.style.setProperty('--text-color-nav', '#ffffff');
        r.style.setProperty('--secondary-color-nav', '#76abff');

        r.style.setProperty('--main-color', '#ffffff');
        r.style.setProperty('--text-color', '#333333');
        r.style.setProperty('--secondary-color', '#76abff');
        mode.innerHTML = "Dark-Mode";
      }
  }