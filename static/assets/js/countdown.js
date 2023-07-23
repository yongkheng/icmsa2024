

function timer() {
  return {
    days: "00",
    hours: "00",
    minutes: "00",
    seconds: "00",
    endTime: new Date(
      "May 27, 2024 23:59:59 GMT+8"
    ).getTime(),
    now: new Date().getTime(),
    timeLeft: 0,
    countdown: function () {
      let counter = setInterval(() => {
        this.now = new Date().getTime();
        this.timeLeft = (this.endTime - this.now) / 1000;
        this.seconds = this.format(this.timeLeft % 60);
        this.minutes = this.format(this.timeLeft / 60) % 60;
        this.hours =
          this.format(this.timeLeft / (60 * 60)) % 24;
        this.days = this.format(
          this.timeLeft / (60 * 60 * 24)
        );
        if (this.timeLeft <= 0) {
          clearInterval(counter);
          this.seconds = "00";
          this.minutes = "00";
          this.hours = "00";
          this.days = "00";
        }
      }, 1000);
    },
    format: function (value) {
      if (value < 10) {
        return "0" + Math.floor(value);
      } else return Math.floor(value);
    },
  };
}
