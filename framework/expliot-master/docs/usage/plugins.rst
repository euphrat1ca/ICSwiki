Plugins/Test cases
==================

The framework consists of various plugins which are either exploits or for
recon, analysis, etc. Each plugin executes a specific test case. These test
cases are the basis of automation of security/regression testing for IoT
products and infrastructure. The name of a plugin, as seen on the framework's
console, is a *unique identifier* (ID) which identifies the plugin's
capabilities and the target.

Plugin IDs
----------

The plugins are identified and categorized using their IDs and have a specific
format. The IDs are unique within the framework. They are comprised of three
components. 

- Protocol or the technology it targets.
- Product that it targets.
- Name of the of the plugin itself that describes its action.

The format of the ID is ``protocol.product.plugin_name``.

For example, the ID of the BLE scanner plugin is ``ble.generic.scan``. Since it
is a generic BLE scanner and not specific to any BLE product, the product 
component of the ID is *generic*.
