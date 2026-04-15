export default function Panel({ title, right, children }) {
  return (
    <section className="panel">
      <header className="panel-header">
        <h2>{title}</h2>
        {right ? <div>{right}</div> : null}
      </header>
      {children}
    </section>
  );
}