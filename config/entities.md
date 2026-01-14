# Entity Definitions

This document outlines the entities to be created in DialogFlow CX.

## Entity 1: City (Custom Entity)

**Purpose**: Extract city names from user utterances for weather queries.

### Entity Type
- Custom Entity (or use @sys.geo-city system entity)

### Values and Synonyms

| Value | Synonyms |
|-------|----------|
| New York | NYC, New York City, NY |
| London | Greater London, London UK |
| Tokyo | Tokyo Japan, 東京 |
| Paris | Paris France, City of Light |
| San Francisco | SF, San Fran, Bay Area |
| Seattle | Emerald City |
| Miami | Miami Beach, South Beach |
| Dubai | Dubai UAE, دبي |
| Boston | Beantown |
| Chicago | Windy City, Chi-Town |
| Los Angeles | LA, Los Angeles CA, City of Angels |
| Sydney | Sydney Australia |
| Toronto | Toronto Canada, TO |
| Berlin | Berlin Germany |
| Mumbai | Bombay, Mumbai India |

### Configuration
- **Match Mode**: Fuzzy matching enabled
- **Auto Expansion**: Enabled (to catch variations)
- **Redacted**: No

---

## Entity 2: Name (Custom Entity)

**Purpose**: Extract person names from greetings and introductions.

### Entity Type
- Custom Entity (or use @sys.person system entity)

### Values and Synonyms

| Value | Synonyms |
|-------|----------|
| John | Johnny, Jon |
| Sarah | Sara, Sally |
| Mike | Michael, Mikey |
| Emily | Em, Emma |
| David | Dave, Davy |

### Configuration
- **Match Mode**: Exact match
- **Auto Expansion**: Disabled
- **Redacted**: No (for personalized responses)

**Note**: For production, consider using @sys.person system entity which has better coverage.

---

## Entity 3: WeatherCondition (Custom Entity)

**Purpose**: Extract weather-related terms for better intent understanding.

### Entity Type
- Custom Entity

### Values and Synonyms

| Value | Synonyms |
|-------|----------|
| temperature | temp, degrees, how hot, how cold |
| humidity | moisture, dampness |
| rain | raining, rainy, precipitation |
| sunny | sun, sunshine, clear |
| cloudy | clouds, overcast |
| windy | wind, breezy |
| snow | snowing, snowy, snowfall |

### Configuration
- **Match Mode**: Fuzzy matching enabled
- **Auto Expansion**: Enabled
- **Redacted**: No

---

## System Entities to Use

DialogFlow CX provides several system entities that can be used:

1. **@sys.geo-city**: For city names (alternative to custom City entity)
2. **@sys.person**: For person names (alternative to custom Name entity)
3. **@sys.date**: For date references
4. **@sys.time**: For time references
5. **@sys.number**: For numeric values
6. **@sys.unit-currency**: For currency amounts

## Best Practices

1. **Use System Entities When Possible**: System entities have better coverage and are maintained by Google
2. **Add Comprehensive Synonyms**: Include common variations, abbreviations, and alternative names
3. **Test Entity Extraction**: Verify entities are correctly extracted from various phrasings
4. **Consider Fuzzy Matching**: Enable for entities with many variations (like city names)
5. **Update Regularly**: Add new values and synonyms based on user interactions
