javascript:(function() {
  const params = new URLSearchParams(window.location.search);
  const currentQuery = params.get('q');

  if (currentQuery) {
    // List of engines you want to open
    const engines = [
      'https://duckduckgo.com/?q=',
      'https://bing.com/search?q=',
      'https://search.yahoo.com/search?p='
    ];

    // Stagger each pop-up by a small delay
    engines.forEach((engine, index) => {
      setTimeout(() => {
        window.open(engine + encodeURIComponent(currentQuery), '_blank');
      }, index * 1000);
    });

  } else {
    alert('No search query found in the URL.');
  }
})();