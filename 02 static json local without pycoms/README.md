## Load a local JSON file and use it to populate an experiment

### Conditions
1. Local JSON file
2. Local AnyLogic client
3. No nested data

### Requirements
1. Uses the `jackson` library to parse JSON files to Java

*Can be found in main > Advanced Java*
``` java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.TextNode;
import com.fasterxml.jackson.databind.node.NumericNode;
```

*and some standard Java IO stuff for reading the local file as a string*
```java
import java.io.File;
import java.io.IOException;
```


### Procedure

1. If you want, you can use `create_custom_input.py` again to tailor the size of the input to your liking. 
2. Open the AnyLogic model

    On `main` the function `loadFromJson` is called on startup:  
    *The first part loads the JSON string using the `jackson` module*
    ```java
     // create a mapper to parse the JSON file
   ObjectMapper mapper = new ObjectMapper();

   // open the json file using java.io.File and cast it to an ArrayList (because current
   // JSON format is encapsulated in an array that represents all households)
   try {
   	parsedJSON = mapper.readValue(
   			new File(".\\custom_input.json"),
   			ArrayList.class);

   } catch (IOException e) {
   	e.printStackTrace();
   }
    ```

    *The second part parses the entries of the ArrayList to Hashmaps (key:value pairs) of types `<string>:<object>`. This is subsequently parsed to the types explicitly stated by the Household agent-type.*

    ```Java
   // iterate over the entries in the ArrayList as HashMaps so we can access the 
   // values by calling the corresponding keys
   for (HashMap<String, Object> data : parsedJSON) {
   	String house_type = (String) data.get("house_type");
   	String heating_type = (String) data.get("heating_type");
   	int number_of_residents = (int) data.get("number_of_residents");
   	
   	// Initiate the household in the population
   	Household newHousehold = add_households(house_type,
   			heating_type, number_of_residents);

   }
    ```

    3. Run the model and use the '**print input json**' button to inspect the input file parsed to an `ArrayList`
    ```java
      int val = 0;

      while (parsedJSON.size() > val ){
      	traceln(parsedJSON.get(val));
      	val++;
      }
    ```

    4. Outputs are parsed to JSON using a template Java Class (pojo even?): `Results.java`, that links the household parameters of interest (in this case all) to a plain Java object. To this end, the most important part is the implementation of the constructor in `Results.java`

   ``` Java
       /**
        * Constructor initializing the fields
        */
       public Results(String heatingType, String houseType, int numberOfResidents) {
   		this.heatingType = heatingType;
   		this.houseType = houseType;
   		this.numberOfResidents = numberOfResidents;
       }
   ```
   5. This is used by the '**print output json**' button. First an empty array is initialized. Entries are added to this `ArrayList` by iterating over the `households` population.  The required values for the constructor of the `Results` class are passed by attribute access the parameters of the `Household` instances.
   ``` java

   ObjectMapper mapper = new ObjectMapper();

   ArrayList<Results> result_array = new ArrayList();

   for (Household h : households) {
   	result_array.add(new Results(h.heating_type,
   			h.house_type, h.number_of_residents)

   	);

   }
   
   // Uses pretty print for readeability
   try {
   	String jsonString = mapper
   			.writerWithDefaultPrettyPrinter().writeValueAsString(result_array);
   	traceln(jsonString);

   } catch (IOException e) {
   	e.printStackTrace();
   }
```


---
A useful [blog](https://mkyong.com/java/jackson-how-to-parse-json/) article on Java and JSON parsing.