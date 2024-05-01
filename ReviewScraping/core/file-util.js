const fs = require("fs");

class FileUtil {
  constructor(writeStream) {
    this._writeStream = writeStream;
  }

  appendLine(content, addNewLine = true) {
    this._writeStream.write(content + (addNewLine ? "\n" : ""));
  }
}

module.exports = FileUtil;
