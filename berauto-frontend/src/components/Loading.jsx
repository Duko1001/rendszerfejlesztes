export default function Loading({ text = 'Betöltés...' }) {
  return <div className="loading"><div className="spinner" />{text}</div>;
}
