export function timeDiffFromNow(date) {
    let seconds = (new Date().getTime() - new Date(date).getTime()) / 1000
    let d = Math.floor(seconds / (3600 * 24));
    let h = Math.floor(seconds % (3600 * 24) / 3600);
    let m = Math.floor(seconds % 3600 / 60);
    let s = Math.floor(seconds % 60);

    let dDisplay = d ? d + (d == 1 ? " day, " : " days, ") : "";
    let hDisplay = h ? h + (h == 1 ? " hour, " : " hours, ") : "";
    let mDisplay = m ? m + (m == 1 ? " minute, " : " minutes, ") : "";
    let sDisplay = s ? s + (s == 1 ? " second" : " seconds") : "";
    return dDisplay + hDisplay + mDisplay + sDisplay;
}
