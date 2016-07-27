import java.io.*;
import javax.xml.validation.*;
import javax.xml.transform.stream.StreamSource;
import javax.xml.transform.Source;
import org.xml.sax.SAXException;
import javax.xml.XMLConstants;

/**
 * Sets up a XSD validator for IMDI files.
 *
 * @author Anna Jancso
 */
public class XSDValidator {

    private Validator validator;


    /**
    * Sets XSD validator with a XSD file.
    *
    * @param xsdFile XSD file
    */
    private void setValidator(File xsdFile) throws SAXException {
        SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
        Schema schema = factory.newSchema(xsdFile);
        validator = schema.newValidator();
    }

    /**
     * Validates a IMDI files against a XSD file.
     *
     * @param imdiFile IMDI file to be checked
     */
    public void validate(File imdiFile) throws SAXException, IOException {

        Source source = new StreamSource(imdiFile);

        Boolean is_valid = true;

        try { validator.validate(source); }
        catch (SAXException exc) {
            System.out.println(imdiFile.getName() + " is not valid:");
            System.out.println(exc.getMessage());
            is_valid = false;
        }

        if (is_valid) {
            System.out.println(imdiFile.getName() + " is valid");
        }
    }

    /**
     * Validates all IMDI files against a xsd file.
     *
     * @param args first argument: path to XSD file
     *             second argument: path to directory containing all IMDI files
     */
    public static void main(String[] args) throws SAXException, IOException {

        // number of arguments given over command line
        int argsLength = args.length;

        // default paths
        String xsdPath = "../Metadata/imdi-session.xsd";
        String imdiPath = "../Metadata/IMDI";

        // overwrite them if they were given over command line
        if (argsLength == 1) { xsdPath = args[0]; }
        else if (argsLength == 2) {
            xsdPath = args[0];
            imdiPath = args[1];
        }

        File xsdFile = new File(xsdPath);
        File imdiFile = new File(imdiPath);

        // set validator with XSD file
        XSDValidator validator = new XSDValidator();
        validator.setValidator(xsdFile);

        // get all files in IMDI directory
        File[] imdiFiles = imdiFile.listFiles();

        // validate every IMDI file against the XSD
        for (File file : imdiFiles) { validator.validate(file); }
    }
}
