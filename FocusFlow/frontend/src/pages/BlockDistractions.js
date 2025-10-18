import BlockerSettings from '../components/BlockerSettings';

function BlockDistractions() {
  return (
    <div className="container">
      <h2>Block Distractions</h2>
      <p>Manage the sites and apps you want to block during focus sessions.</p>
      <BlockerSettings />
    </div>
  );
}

export default BlockDistractions;
