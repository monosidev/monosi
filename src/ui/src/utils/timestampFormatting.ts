import { format } from 'date-fns';

const DEFAULT_TIMESTAMP_FORMAT: string = 'eeee, MMM do (HH:mm:ss)';

const formatTimestamp = (
  timestamp: string,
  tFormat: string = DEFAULT_TIMESTAMP_FORMAT
) => {
  try {
    const formattedDate = format(new Date(timestamp), tFormat);
    return formattedDate;
  } catch (e) {
    return timestamp;
  }
};

export { DEFAULT_TIMESTAMP_FORMAT, formatTimestamp };
