function getDayOfYear(date) {
  const start = Date.UTC(date.getUTCFullYear(), 0, 0);
  const end = Date.UTC(date.getUTCFullYear(), date.getUTCMonth(), date.getUTCDate());
  return Math.floor((end - start) / 86400000);
}