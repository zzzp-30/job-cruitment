const timeStampFormat = (time: string) => {
  const dateTime = new Date(time);
  const YY = String(dateTime.getFullYear()).padStart(4, '0');
  const MM = String(dateTime.getMonth() + 1).padStart(2, '0');
  const DD = String(dateTime.getDate()).padStart(2, '0');
  const hh = String(dateTime.getHours()).padStart(2, '0');
  const mm = String(dateTime.getMinutes()).padStart(2, '0');
  const ss = String(dateTime.getSeconds()).padStart(2, '0');
  return `${YY}/${MM}/${DD} ${hh}:${mm}:${ss}`;
};

export { timeStampFormat }