const getASINWithRegex = (url) => {
  // regex from https://stackoverflow.com/a/62343336/7010492
  let regex = RegExp("(?:[/])([A-Z0-9]{10})(?:[/|?|&|s])");
  let parts = url.match(regex);
  if (parts && parts.length > 0) {
    return parts[0].replace(/\//g, "");
  }
  return null; // if there is nothing
};

module.exports = {
  getASINWithRegex,
};
