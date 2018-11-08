---
---
async function init() {
  try {
    const data = await Promise.all([
      fetch('{{ site.baseurl }}/translations.json')
        .then((response) => response.json()),
      fetch('{{ site.baseurl }}/contexts.json')
        .then((response) => response.json())
    ]);
    const languages = data[0];
    const contexts = data[1];
    // Convert the json into an array of documents for Lunr to index.
    let docs = {};
    Object.entries(languages).map(([lang, groups]) => {
      if (groups) {
        Object.entries(groups).map(([group, keys]) => {
          if (keys) {
            Object.entries(keys).map(([key, val]) => {
              // Support either objects of strings, or just strings.
              if (typeof val === 'object') {
                Object.entries(val).map(([subkey, subval]) => {
                  const doc_key = group + ':' + key + '---' + subkey;
                  if (!docs[doc_key]) {
                    docs[doc_key] = {};
                  }
                  docs[doc_key]['key'] = doc_key;
                  docs[doc_key][lang] = subval;
                });
              }
              else {
                const doc_key = group + ':' + key;
                if (!docs[doc_key]) {
                  docs[doc_key] = {};
                }
                docs[doc_key]['key'] = doc_key;
                docs[doc_key][lang] = val;
              }
            });
          }
        });
      }
    });
    // Add any contextual info.
    contexts.forEach(function(context) {
      if (docs[context.key]) {
        docs[context.key]['context'] = context.context;
      }
    });
    // Set up the Lunr index.
    const idx = lunr(function() {
      this.ref('key');
      this.field('key');
      this.field('context');
      Object.keys(languages).forEach(function(lang) {
        this.field(lang);
      }, this);
      Object.values(docs).forEach(function(doc) {
        this.add(doc);
      }, this);
    });
    // Apply behavior to search input.
    const search_bar = document.getElementById('search-bar');
    const search_results = document.getElementById('search-results');
    search_bar.addEventListener('keyup', function(e) {
      if (this.value.length > 3) {
        // Escape colons since we use them in translation keys.
        const search_query = this.value.replace(":", "\\:");
        const matches = idx.search(search_query);
        let results = '<p>No translations found.</p>';
        if (matches.length) {
          results = '';
          matches.forEach(function(match) {
            results += '<pre>' + JSON.stringify(docs[match.ref], null, 2) + '</pre>';
          });
        }
        search_results.innerHTML = results;
      }
    });
  }
  catch (error) {
    console.log(error);
  }
}
init();