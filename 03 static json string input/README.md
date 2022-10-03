## Load a local JSON file and use it to populate an experiment

## Key findings

1. Strings can be used as input parameters that are later parsed to JSON / `Array<Hashmap>` types. 
2. Java / AnyLogic has requirements on string escape chars for interior quotes. 
3. I was able to push the number of households to 1200 (~120kb of data), but got a weird display bug inside the default value window. Compiled&ran without errors with expected functionalities.  

### Conditions
1. In workspace static JSON-like string variable
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
import java.io.IOException;
```


### Procedure

1. `create_custom_input.py` is ran again, but `json.dumps` is used to control the string output format with some subsequent modifications before writing to a text file. 
    ```python
    str = json.dumps(output, cls=EnhancedJSONEncoder)
    str = str.replace('"', r"\"")
    str = '"' + str + '"'
    with open("custom_input.txt", "w") as outfile:
        outfile.writelines([str])
    ```
2. Open the AnyLogic model
    The `main` now includes a new parameter; the `rawString`. This is of type `String` and includes a string formatted in JSON while Java character escapes are respected (e.g. within the opening `"` subsequent nested `"` are precedented by a slash char yielding `\"` around keys)

    The `loadFromJson` on `main` is largely unaltered (the `File` input function is exchanged for a parameter `rawString`. The function is still called on startup:  
    ```java
     // create a mapper to parse the JSON file
   ObjectMapper mapper = new ObjectMapper();

   // open the json file using java.io.File and cast it to an ArrayList (because current
   // JSON format is encapsulated in an array that represents all households)
   try {
   	parsedJSON = mapper.readValue(
   			rawString,    // <--- THIS PART CHANGED!
   			ArrayList.class);

   } catch (IOException e) {
   	e.printStackTrace();
   }
    ```
    _This also removes the need for the `java.IO.File` import requirement_   
    **From here onwards the code is unaltered from the previous experiment**
  ---


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

 2. Run the model and use the '**print input json**' button to inspect the input file parsed to an `ArrayList`
   
    ```java
      int val = 0;

      while (parsedJSON.size() > val ){
      	traceln(parsedJSON.get(val));
      	val++;
      }
    ```

    1. Outputs are parsed to JSON using a template Java Class (pojo even?): `Results.java`, that links the household parameters of interest (in this case all) to a plain Java object. To this end, the most important part is the implementation of the constructor in `Results.java`

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
   1. This is used by the '**print output json**' button. First an empty array is initialized. Entries are added to this `ArrayList` by iterating over the `households` population.  The required values for the constructor of the `Results` class are passed by attribute access the parameters of the `Household` instances.
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