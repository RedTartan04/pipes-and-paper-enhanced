document.addEventListener('keydown', on_key_press);

// Mapping between key press events codes and actions
const keyevents = {
  13: "ROTATE",
  32: "CLEAR",
  48: "ERASE",
  68: "DEBUG",
  49: "BLACK",
  50: "ORANGE",
  51: "SKY_BLUE",
  52: "GREEN",
  53: "YELLOW",
  54: "BLUE",
  55: "VERMILLON",
  56: "PURPLE",
};

// Mapping between actions and RGB colors
const pencolors = {
  "BLACK": "rgb(0, 0, 0)",
  "ORANGE": "rgb(230, 159, 0)",
  "SKY_BLUE": "rgb(86, 180, 233)",
  "GREEN": "rgb(0, 158, 115)",
  "YELLOW": "rgb(240, 228, 66)",
  "BLUE": "rgb(0, 114, 178)",
  "VERMILLON": "rgb(213, 94, 0)",
  "PURPLE": "rgb(204, 121, 167)",
}

function on_key_press(e) {
  let action = keyevents[e.keyCode];
  switch (action) {
    case "ROTATE":
      rotate = !rotate;
      let oldWidth = canvas.width;
      canvas.width = canvas.height;
      canvas.height = oldWidth;
      break;
    case "CLEAR":
      canvas.width = canvas.width;
      e.preventDefault();
      break;
    case "ERASE":
      penColor = "";
      break;
    case "DEBUG":
      debug = !debug;
      break;
    default:
      if (action in pencolors) {
        penColor = pencolors[action];
        document.getElementById("pencolor").style.background = pencolors[action];
      }
  }
}
