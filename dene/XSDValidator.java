import java.io.*;
import javax.xml.validation.*;
import javax.xml.transform.stream.StreamSource;
import javax.xml.transform.Source;
import org.xml.sax.SAXException;
import javax.xml.XMLConstants;


public class XSDValidator {

    private File xsdFile;

    public XSDValidator(String xsdPath) { xsdFile = new File(xsdPath); }

    private void validate(String xmlPath) throws SAXException, IOException {

        File xmlFile = new File(xmlPath);

        SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);

        Schema schema = factory.newSchema(xsdFile);

        Validator validator = schema.newValidator();

        Source source = new StreamSource(xmlFile);

        try { validator.validate(source); }
        catch (SAXException exc) {
            System.out.println(xmlFile.getName() + " is not valid:");
            System.out.println(exc.getMessage());
        }
    }

    public static void main(String args[]) throws SAXException, IOException {
        XSDValidator validator = new XSDValidator("imdi-session.xml");
        validator.validate("testset/IMDI/deslas-AMM-2015-06-02.cmdi");
    }

}
