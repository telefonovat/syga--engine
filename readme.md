# Engine

### Todo

#### Workflow & Konvencie

- [x] <s>Upraviť všetky *.py súbory, aby mali 10/10 v Pylint</s>
- [x] <s>Setup Gitlab CI s Pylint a testami</s>
- [ ] Rozlíšiť private a public properties a methods pomocou prefixu _
- [ ] Používať template string, tj. `f''`
- [ ] Rozdeliť utils module
- [ ] Jedna medzera po class docstring-u

#### Testy

- [ ] Unit testy pre `engine`
- [ ] Unit testy pre `runner`
- [ ] Unit testy pre `sender`
- [ ] <s>Unit testy pre `loader`</s> (niektoré už sú, pridať viac)
- [ ] Pozrieť sa neskôr na test_color.py a skontrolovať kvalitu

#### Iné

- [ ] Support pre RGB farby ako string
- [ ] Vytvoriť dedikované Exceptions pre Visualizer, GraphNodeColorizer, ...
- [ ] Implementovať timer (sledovanie času behu algoritmu)
- [ ] <s>Implementovať možnosť špecifikovať uid behu algoritmu (musí to byť chránené heslom)</s> Otestovať to
- [ ] `engine.Color` namiesto importovaného Color (pokojne stačí wrapper)
