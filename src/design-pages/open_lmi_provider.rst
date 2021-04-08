OpenLMI provider design
=======================

Problem Statement
-----------------

SSSD provider for OpenLMI will allow administrators to retrieve
information from SSSD and modify the configuration through OpenLMI
tools.

First iteration
---------------

The first iteration will implement the following features:

-  provide basic information about domains
-  provide methods for changing debug level
-  provide methods for enable/disable services
-  provide methods for enable/disable domains

Implementation design
---------------------

Overview
--------

The OpenLMI provide will use `​D-Bus
responder <https://docs.pagure.org/SSSD.sssd/design_pages/dbus_responder.html>`__
for communication with SSSD. The provider will implement SSSD CIM schema,
which describes the objects and their properties and methods. The schema
should define a low level model of SSSD architecture. To simplify the
most common tasks, we will also implement several python scripts
that will follow the OpenLMI scripts interface. That will allow to run
these scripts as single command from the command line via *lmi* tool.

LMI scripts design
------------------

The LMI scripts are python scripts that should provide a high level
approach to the most common task of the LMI provider. These scripts are
executed from command line using *lmi* tool with *lmi command subcommand
--arg* syntax.

-  **lmi sssd** ::

       # print SSSD service status using LMI_Service provider
       lmi sssd status

       # restart SSSD service using LMI_Service provider
       lmi sssd restart

       # change debug level for selected components (all by default), either permanently (default) or temporarily until SSSD is restarted
       lmi sssd set-debug-level $level [--permanently|--until-restart] [--monitor] [--services=svc1,svc2,...] [--domains=dom1,dom2,...]

-  **lmi sssd-domain** command will provide information about SSSD
   domains ::

       # list SSSD domain with basic information (name, enabled/disabled, id provider), by default only top level domains are listed
       lmi sssd-domain list [--enabled|--disabled] [--with-subdomains]
       lmi sssd-domain enable $domain
       lmi sssd-domain disable $domain

       # prints all available information about the $domain
       lmi sssd-domain info $domain

-  **lmi sssd-service** command will provide information about SSSD
   services ::

       # list SSSD services with basic information (name, enabled/disabled), by default only top level domains are listed
       lmi sssd-service list [--enabled|--disabled]
       lmi sssd-service enable $service
       lmi sssd-service disable $service

       # prints all available information about the $service
       lmi sssd-service info $service

CIM schema
----------

The CIM schema described the interface of OpenLMI SSSD provider. It
defines a low level conceptual model that follows SSSD architecture.

.. FIXME: The image of the UML diagram is missing.
.. UML diagram
.. ~~~~~~~~~~~

MOF
~~~

::

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Description("System Security Services Daemon")]
    class LMI_SSSDService : CIM_Service
    {

    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Abstract, Description("Base class for SSSD's components.")]
    class LMI_SSSDComponent : CIM_ManagedElement
    {
        [Key, Description("Name of the SSSD component.")]
        string Name;

        [Description("Type of the SSSD component."),
         ValueMap { "0", "1", "2" },
         Values { "Monitor", "Responder", "Backend" }]
        uint16 Type;

        [BitValues{"Reserved",
                   "Reserved",
                   "Reserved",
                   "Reserved",
                   "Fatal failures",
                   "Critical failures",
                   "Operation failures",
                   "Minor failures",
                   "Configuration settings",
                   "Function data",
                   "Trace function",
                   "Reserved",
                   "Trace libraries",
                   "Trace internal",
                   "Trace all",
                   "Reserved"},
         Description("Debug level used within this component.")]
        uint16 DebugLevel;

        [Description("True if this process is enabled at SSSD startup and false "
                     "otherwise.")]
        boolean IsEnabled;

        [Description("Permanently change debug level of this component."),
         ValueMap { "0", "1", "2", "3" },
         Values { "Success", "Failed", "Invalid arguments", "I/O error" }]
        uint32 SetDebugLevelPermanently([In] uint16 debug_level);

        [Description("Change debug level of this component but switch it back "
                     "to the original value when SSSD is restarted."),
         ValueMap { "0", "1", "2", "3" },
         Values { "Success", "Failed", "Invalid arguments", "I/O error" }]
        uint32 SetDebugLevelTemporarily([In] uint16 debug_level);

        [Description("Enable this component. SSSD has to be restarted in order "
                     "this change to take any effect."),
         ValueMap { "0", "1", "3" },
         Values { "Success", "Failed", "I/O error" }]
        uint32 Enable();

        [Description("Disable this component. SSSD has to be restarted in order "
                     "this change to take any effect."),
         ValueMap { "0", "1", "3" },
         Values { "Success", "Failed", "I/O error" }]
        uint32 Disable();
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Description("SSSD monitor. An SSSD component that executes the other "
                 "components and makes sure they stay running. This component "
                 "can not be disabled.")]
    class LMI_SSSDMonitor : LMI_SSSDComponent
    {

    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Description("SSSD responder. An SSSD component that implements one of the "
                 "supported services and provides data to clients.")]
    class LMI_SSSDResponder : LMI_SSSDComponent
    {

    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Description("SSSD backend. An SSSD component that manages data from one "
                 "domain and its subdomains.")]
    class LMI_SSSDBackend : LMI_SSSDComponent
    {

    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Description("Data provider module information.")]
    class LMI_SSSDProvider
    {
        [Key, Description("Name of data class handled by the provider.")]
        string Type;

        [Key, Description("Name of the module that provides the desired data.")]
        string Module;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"),
     Description("SSSD domain.")]
    class LMI_SSSDDomain : CIM_ManagedElement
    {
        [Key, Description("Name of the domain.")]
        string Name;

        [Description("List of primary servers for this domain.")]
        string PrimaryServers[];

        [Description("List of backup servers for this domain.")]
        string BackupServers[];

        [Description("The Kerberos realm this domain is configured with.")]
        string Realm;

        [Description("The domain forest this domain belongs to.")]
        string Forest;

        [Description("Name of the parent domain. It is not set if this "
                     "domain is on top of the domain hierarchy.")]
        string ParentDomain;

        [Description("True if this is an autodiscovered subdomain.")]
        boolean IsSubdomain;

        [Description("Minimum UID and GID value for this domain.")]
        uint32 MinId;

        [Description("Maximum UID and GID value for this domain.")]
        uint32 MaxId;

        [Description("True if this domain supports enumeration.")]
        boolean Enumerate;

        [Description("True if objects from this domain can be accessed only via "
                     "fully qualified name.")]
        boolean UseFullyQualifiedNames;

        [Description("The login format this domain expects.")]
        string LoginFormat;

        [Description("Format of fully qualified name this domain uses.")]
        string FullyQualifiedNameFormat;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"), Association,
     Description("All available SSSD components.")]
    class LMI_SSSDAvailableComponent
    {
        [Key, Min(1), Max(1)]
        LMI_SSSDService REF SSSD;

        [Key]
        LMI_SSSDComponent REF Component;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"), Association,
     Description("Data provider modules configured for given backend.")]
    class LMI_SSSDBackendProvider
    {
        [Key, Max(1)]
        LMI_SSSDBackend REF Backend;

        [Key]
        LMI_SSSDProvider REF Provider;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"), Association,
     Description("All domains managed by SSSD.")]
    class LMI_SSSDAvailableDomain
    {
        [Key, Min(1), Max(1)]
        LMI_SSSDService REF SSSD;

        [Key]
        LMI_SSSDDomain REF Domain;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"), Association,
     Description("All top level domains associated with given backend.")]
    class LMI_SSSDBackendDomain
    {
        [Key, Max(1)]
        LMI_SSSDBackend REF Backend;

        [Key, Max(1)]
        LMI_SSSDDomain REF Domain;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"), Association,
     Description("All subdomains associated with given parent domain.")]
    class LMI_SSSDDomainSubdomain
    {
        [Key, Max(1)]
        LMI_SSSDDomain REF ParentDomain;

        [Key]
        LMI_SSSDDomain REF Subdomain;
    };

    [Version("0.1.0"), Provider("cmpi:cmpiLMI_SSSD"), Association]
    class LMI_HostedSSSDService: CIM_HostedService
    {
      [Override("Antecedent"),
       Description("The hosting System.") ]
      CIM_ComputerSystem REF Antecedent;

      [Override("Dependent"),
       Description("Instance of SSSD service.")]
      LMI_SSSDService REF Dependent;
    };

Authors
-------

-  Pavel Březina <`pbrezina@redhat.com <mailto:pbrezina@redhat.com>`__>

.. .. |image0| image:: https://fedorahosted.org/sssd/raw-attachment/wiki/DesignDocs/OpenLMIProvider/uml.png
..    :target: https://fedorahosted.org/sssd/attachment/wiki/DesignDocs/OpenLMIProvider/uml.png
