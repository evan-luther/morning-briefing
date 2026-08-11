import * as SunCalc from "suncalc";
import renderGradient from "../vendor/horizon/src/gradient";

const PHILADELPHIA = { latitude: 39.9526, longitude: -75.1652 };
const timeNode = document.querySelector<HTMLElement>("#localTime");
const greetingNode = document.querySelector<HTMLElement>("#greeting");

function displayDate(): Date {
  const params = new URLSearchParams(location.search);
  if (params.get("og") !== "1") return new Date();
  const now = new Date();
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).formatToParts(now);
  const value = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return new Date(`${value.year}-${value.month}-${value.day}T07:00:00-04:00`);
}

function updateSky(): void {
  const now = displayDate();
  const sun = SunCalc.getPosition(now, PHILADELPHIA.latitude, PHILADELPHIA.longitude);
  const [gradient, top, bottom] = renderGradient(sun.altitude);
  const luminance = (rgb: number[]) => 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2];
  const average = (luminance(top) + luminance(bottom)) / 2;
  const lightInk = average < 142;

  document.documentElement.style.setProperty("--horizon", gradient);
  document.documentElement.style.setProperty("--ink", lightInk ? "#f5f7f8" : "#17212a");
  document.documentElement.style.setProperty("--muted", lightInk ? "rgba(245,247,248,.68)" : "rgba(23,33,42,.62)");
  document.documentElement.style.setProperty("--line", lightInk ? "rgba(245,247,248,.25)" : "rgba(23,33,42,.20)");
  document.documentElement.style.setProperty("--shadow", lightInk ? "rgba(6,12,18,.28)" : "rgba(255,255,255,.18)");
}

function updateClock(): void {
  const now = displayDate();
  const hour = Number(new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York",
    hour: "numeric",
    hour12: false,
  }).format(now));
  const period = hour < 12 ? "morning" : hour < 18 ? "afternoon" : "evening";
  if (greetingNode) greetingNode.textContent = `Good ${period}.`;
  if (timeNode) {
    timeNode.textContent = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/New_York",
      hour: "numeric",
      minute: "2-digit",
    }).format(now);
  }
}

updateSky();
updateClock();
setInterval(() => {
  updateSky();
  updateClock();
}, 60_000);
