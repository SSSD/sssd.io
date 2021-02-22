Common IPA Provider issues
##########################

* In an IPA-AD trust setup, ``getent group $groupname`` doesn't display any group members of an AD group
* In an IPA-AD trust setup, ``id $username`` doesn't display any groups for an AD user
  * This is expected with very old SSSD and FreeIPA versions. In order to display the group members for groups and groups for user, you need to have at least SSSD 1.12 on the client and FreeIPA server 4.1 or newer at the same time
* In an IPA-AD trust setup, IPA users can be resolved, but AD trusted users can't
  * The IPA client machines query the SSSD instance on the IPA server for AD users. If the client logs contain errors such as:

      .. code-block:: sssd-log

            [ipa_s2n_exop_done] (0x0040): ldap_extended_operation result: Operations error(1), Failed to handle the request.

        or:

            [ipa_s2n_get_user_done] (0x0040): s2n exop request failed.


      * Check if AD trusted users be resolved on the server at least. Enable debugging for the SSSD instance on the IPA server and take a look at SSSD logs there. Chances are the SSSD on the server is misconfigured or maybe not running at all - make sure that all the requests towards the NSS responder can be answered on the server.

* In an IPA-AD trust setup, AD trust users cannot be resolved or secondary groups are missing on the IPA server
  *  This can be caused by AD permissions issues if the below errors are seen in the logs:

      .. code-block:: sssd-log

            [sdap_ad_resolve_sids_done] (0x0020): Unable to resolve SID S-1-5-21-101891098-1139187330-4192773280-XXXXXX - will try next sid.

      * Validate permissions on the AD object printed in the logs. This can checked by manually performing ldapsearch with the same LDAP filter and kerberos credentials that SSSD uses(one-way trust uses keytab in ``/var/lib/sss/keytabs/`` and two-way trust uses host principal in ``/etc/krb5.keytab``).

* In an IPA-AD trust setup, IPA users can log in, but AD users can't

  * Unless you use a "legacy client" such as ``nss_ldap``, then IPA users authenticate against the IPA server, but AD users authenticate against the AD servers directly. Therefore, you can test the authentication directly with ``kinit``. Use ``KRB5_TRACE`` for extra tracing information.
* HBAC rules keep denying access.

  * Use the ``ipa hbactest`` utility on the IPA server to see if the user is permitted access. The SSSD uses the same code as ``ipa hbactest``
* In an IPA-AD trust setup, a user from the AD domain only lists his AD group membership, not the IPA external groups
* HBAC prevents access for a user from a trusted AD domain, where the HBAC rule is mapped to an IPA group via an AD group

  * Make sure the group scope of the AD group mapped to the rule is not domain-local. Domain-local groups can't cross the trust boundary and cannot be therefore used for HBAC rules.
  * Check the keytab on the IPA client and make sure that it only contains entries from the IPA domain. If the keytab contains an entry from the AD domain, the PAC code might pick this entry for an AD user and then the PAC would only contain the AD groups, because the PAC would then be verified with the help of the AD KDC which knows nothing about the IPA groups and removes them from the PAC
  * Check the PAC with the help of a dedicated `IPA wiki page <https://www.freeipa.org/page/Howto/Inspecting_the_PAC>`_ If the PAC contains the group, but it is not displayed on the client, then the issue is on the client side. If the PAC doesn't display the group in the PAC, then the issue is on the IPA KDC side. This would at least enable you to ask better questions on the user support lists.
