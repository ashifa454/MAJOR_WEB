<script type="text/javascript" src="https://www.google.com/jsapi"></script>

<script type="text/javascript">
  google.load("elements", "1", {
  packages: "transliterate"
  });
</script>

google.language.transliterate(["Namaste"], "en", "hi", function(result) {
  if (!result.error) {
    if (result.transliterations && result.transliterations.length > 0 &&
        result.transliterations[0].transliteratedWords.length > 0) {
      var text = result.transliterations[0].transliteratedWords[0];
    }
  }
});