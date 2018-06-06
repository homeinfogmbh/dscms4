# ./dom.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:6153fdd8733ad32a3c6c6645b5e2ca64d0d4be50
# Generated 2018-06-06 11:59:30.872527 by PyXB version 1.2.6-DEV using Python 3.6.5.final.0
# Namespace http://xml.homeinfo.de/schema/presentation

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:4e5fb380-6970-11e8-8cd3-7427eaa9df7d')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.6-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://xml.homeinfo.de/schema/presentation', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, default_namespace=None, location_base=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword default_namespace The L{pyxb.Namespace} instance to use as the
    default namespace where there is no default namespace in scope.
    If unspecified or C{None}, the namespace of the module containing
    this function will be used.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement, default_namespace=default_namespace)
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=default_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if default_namespace is None:
        default_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, default_namespace)


# Complex type {http://xml.homeinfo.de/schema/presentation}Attachment with content type ELEMENT_ONLY
class Attachment (pyxb.binding.basis.complexTypeDefinition):
    """
                Ein Dateianhang.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Attachment')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 12, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element mimetype uses Python identifier mimetype
    __mimetype = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mimetype'), 'mimetype', '__httpxml_homeinfo_deschemapresentation_Attachment_mimetype', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 19, 12), )

    
    mimetype = property(__mimetype.value, __mimetype.set, None, '\n                        MIME Typ.\n                    ')

    
    # Element filename uses Python identifier filename
    __filename = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'filename'), 'filename', '__httpxml_homeinfo_deschemapresentation_Attachment_filename', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 26, 12), )

    
    filename = property(__filename.value, __filename.set, None, '\n                        Dateiname.\n                    ')

    
    # Attribute sha256sum uses Python identifier sha256sum
    __sha256sum = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'sha256sum'), 'sha256sum', '__httpxml_homeinfo_deschemapresentation_Attachment_sha256sum', pyxb.binding.datatypes.string)
    __sha256sum._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 34, 8)
    __sha256sum._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 34, 8)
    
    sha256sum = property(__sha256sum.value, __sha256sum.set, None, '\n                    SHA-256 Prüfsumme.\n                ')

    _ElementMap.update({
        __mimetype.name() : __mimetype,
        __filename.name() : __filename
    })
    _AttributeMap.update({
        __sha256sum.name() : __sha256sum
    })
_module_typeBindings.Attachment = Attachment
Namespace.addCategoryObject('typeBinding', 'Attachment', Attachment)


# Complex type {http://xml.homeinfo.de/schema/presentation}BaseChart with content type ELEMENT_ONLY
class BaseChart (pyxb.binding.basis.complexTypeDefinition):
    """
                Basis Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'BaseChart')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 15, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__httpxml_homeinfo_deschemapresentation_BaseChart_title', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 22, 12), )

    
    title = property(__title.value, __title.set, None, '\n                        Der Titel des Charts.\n                    ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpxml_homeinfo_deschemapresentation_BaseChart_description', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 29, 12), )

    
    description = property(__description.value, __description.set, None, '\n                        Die Beschreibung des Charts.\n                    ')

    
    # Element duration uses Python identifier duration
    __duration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'duration'), 'duration', '__httpxml_homeinfo_deschemapresentation_BaseChart_duration', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 36, 12), )

    
    duration = property(__duration.value, __duration.set, None, '\n                        Die Anzeigedauer des Charts.\n                    ')

    
    # Element transition uses Python identifier transition
    __transition = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'transition'), 'transition', '__httpxml_homeinfo_deschemapresentation_BaseChart_transition', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 43, 12), )

    
    transition = property(__transition.value, __transition.set, None, '\n                        Übergangseffekt.\n                    ')

    
    # Element created uses Python identifier created
    __created = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'created'), 'created', '__httpxml_homeinfo_deschemapresentation_BaseChart_created', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 50, 12), )

    
    created = property(__created.value, __created.set, None, '\n                        Datum der Erstellung.\n                    ')

    
    # Attribute display_from uses Python identifier display_from
    __display_from = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'display_from'), 'display_from', '__httpxml_homeinfo_deschemapresentation_BaseChart_display_from', pyxb.binding.datatypes.dateTime)
    __display_from._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 58, 8)
    __display_from._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 58, 8)
    
    display_from = property(__display_from.value, __display_from.set, None, '\n                    Anzeigedatum Beginn.\n                ')

    
    # Attribute display_until uses Python identifier display_until
    __display_until = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'display_until'), 'display_until', '__httpxml_homeinfo_deschemapresentation_BaseChart_display_until', pyxb.binding.datatypes.dateTime)
    __display_until._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 65, 8)
    __display_until._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 65, 8)
    
    display_until = property(__display_until.value, __display_until.set, None, '\n                    Anzeigedatum Ende.\n                ')

    _ElementMap.update({
        __title.name() : __title,
        __description.name() : __description,
        __duration.name() : __duration,
        __transition.name() : __transition,
        __created.name() : __created
    })
    _AttributeMap.update({
        __display_from.name() : __display_from,
        __display_until.name() : __display_until
    })
_module_typeBindings.BaseChart = BaseChart
Namespace.addCategoryObject('typeBinding', 'BaseChart', BaseChart)


# Complex type {http://xml.homeinfo.de/schema/presentation}Chart with content type ELEMENT_ONLY
class Chart (pyxb.binding.basis.complexTypeDefinition):
    """
                Abstrakter Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Chart')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 75, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element base uses Python identifier base
    __base = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'base'), 'base', '__httpxml_homeinfo_deschemapresentation_Chart_base', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12), )

    
    base = property(__base.value, __base.set, None, '\n                        Der zugehörige Basis-Chart.\n                    ')

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpxml_homeinfo_deschemapresentation_Chart_id', pyxb.binding.datatypes.positiveInteger)
    __id._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 90, 8)
    __id._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 90, 8)
    
    id = property(__id.value, __id.set, None, '\n                    Die Chart ID.\n                ')

    
    # Attribute type uses Python identifier type
    __type = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpxml_homeinfo_deschemapresentation_Chart_type', pyxb.binding.datatypes.string)
    __type._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 97, 8)
    __type._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 97, 8)
    
    type = property(__type.value, __type.set, None, '\n                    Der Charttyp.\n                ')

    _ElementMap.update({
        __base.name() : __base
    })
    _AttributeMap.update({
        __id.name() : __id,
        __type.name() : __type
    })
_module_typeBindings.Chart = Chart
Namespace.addCategoryObject('typeBinding', 'Chart', Chart)


# Complex type {http://xml.homeinfo.de/schema/presentation}Configuration with content type ELEMENT_ONLY
class Configuration (pyxb.binding.basis.complexTypeDefinition):
    """
                Eine Konfiguration.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Configuration')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 13, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpxml_homeinfo_deschemapresentation_Configuration_name', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 20, 12), )

    
    name = property(__name.value, __name.set, None, '\n                        Name der Konfiguration.\n                    ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpxml_homeinfo_deschemapresentation_Configuration_description', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 27, 12), )

    
    description = property(__description.value, __description.set, None, '\n                        Beschreibung der Konfiguration.\n                    ')

    
    # Element font uses Python identifier font
    __font = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font'), 'font', '__httpxml_homeinfo_deschemapresentation_Configuration_font', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 34, 12), )

    
    font = property(__font.value, __font.set, None, '\n                        Schriftart.\n                    ')

    
    # Element portrait uses Python identifier portrait
    __portrait = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'portrait'), 'portrait', '__httpxml_homeinfo_deschemapresentation_Configuration_portrait', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 41, 12), )

    
    portrait = property(__portrait.value, __portrait.set, None, '\n                        Soll Portrait Darstellung verwendet werden?\n                    ')

    
    # Element touch uses Python identifier touch
    __touch = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'touch'), 'touch', '__httpxml_homeinfo_deschemapresentation_Configuration_touch', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 48, 12), )

    
    touch = property(__touch.value, __touch.set, None, '\n                        Handelt es sich um ein Touch System?\n                    ')

    
    # Element design uses Python identifier design
    __design = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'design'), 'design', '__httpxml_homeinfo_deschemapresentation_Configuration_design', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 55, 12), )

    
    design = property(__design.value, __design.set, None, '\n                        Das verwendete Design.\n                    ')

    
    # Element effects uses Python identifier effects
    __effects = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'effects'), 'effects', '__httpxml_homeinfo_deschemapresentation_Configuration_effects', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 62, 12), )

    
    effects = property(__effects.value, __effects.set, None, '\n                        Sollen Effekte verwendet werden?\n                    ')

    
    # Element ticker_speed uses Python identifier ticker_speed
    __ticker_speed = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ticker_speed'), 'ticker_speed', '__httpxml_homeinfo_deschemapresentation_Configuration_ticker_speed', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 69, 12), )

    
    ticker_speed = property(__ticker_speed.value, __ticker_speed.set, None, '\n                        Geschwindigkeit des Tickers.\n                    ')

    
    # Element colors uses Python identifier colors
    __colors = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'colors'), 'colors', '__httpxml_homeinfo_deschemapresentation_Configuration_colors', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 76, 12), )

    
    colors = property(__colors.value, __colors.set, None, '\n                        Die verwendeten Farben.\n                    ')

    
    # Element title_size uses Python identifier title_size
    __title_size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title_size'), 'title_size', '__httpxml_homeinfo_deschemapresentation_Configuration_title_size', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 83, 12), )

    
    title_size = property(__title_size.value, __title_size.set, None, '\n                        Größe des Titels.\n                    ')

    
    # Element text_size uses Python identifier text_size
    __text_size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text_size'), 'text_size', '__httpxml_homeinfo_deschemapresentation_Configuration_text_size', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 90, 12), )

    
    text_size = property(__text_size.value, __text_size.set, None, '\n                        Größe des Texts.\n                    ')

    
    # Element logo uses Python identifier logo
    __logo = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'logo'), 'logo', '__httpxml_homeinfo_deschemapresentation_Configuration_logo', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 97, 12), )

    
    logo = property(__logo.value, __logo.set, None, '\n                        Firmenlogo.\n                    ')

    
    # Element background uses Python identifier background
    __background = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'background'), 'background', '__httpxml_homeinfo_deschemapresentation_Configuration_background', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 104, 12), )

    
    background = property(__background.value, __background.set, None, '\n                        Hintergrundbild.\n                    ')

    
    # Element dummy_picture uses Python identifier dummy_picture
    __dummy_picture = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'dummy_picture'), 'dummy_picture', '__httpxml_homeinfo_deschemapresentation_Configuration_dummy_picture', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 111, 12), )

    
    dummy_picture = property(__dummy_picture.value, __dummy_picture.set, None, '\n                        Platzhalterbild.\n                    ')

    
    # Element hide_cursor uses Python identifier hide_cursor
    __hide_cursor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hide_cursor'), 'hide_cursor', '__httpxml_homeinfo_deschemapresentation_Configuration_hide_cursor', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 118, 12), )

    
    hide_cursor = property(__hide_cursor.value, __hide_cursor.set, None, '\n                        Soll der Cursor ausgeblendet werden?\n                    ')

    
    # Element rotation uses Python identifier rotation
    __rotation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rotation'), 'rotation', '__httpxml_homeinfo_deschemapresentation_Configuration_rotation', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 125, 12), )

    
    rotation = property(__rotation.value, __rotation.set, None, '\n                        Rotation in Grad.\n                    ')

    
    # Element email_form uses Python identifier email_form
    __email_form = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'email_form'), 'email_form', '__httpxml_homeinfo_deschemapresentation_Configuration_email_form', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 132, 12), )

    
    email_form = property(__email_form.value, __email_form.set, None, '\n                        Soll ein E-Mail Formular angezeigt werden?\n                    ')

    
    # Element volume uses Python identifier volume
    __volume = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'volume'), 'volume', '__httpxml_homeinfo_deschemapresentation_Configuration_volume', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 139, 12), )

    
    volume = property(__volume.value, __volume.set, None, '\n                        Lautstärke.\n                    ')

    _ElementMap.update({
        __name.name() : __name,
        __description.name() : __description,
        __font.name() : __font,
        __portrait.name() : __portrait,
        __touch.name() : __touch,
        __design.name() : __design,
        __effects.name() : __effects,
        __ticker_speed.name() : __ticker_speed,
        __colors.name() : __colors,
        __title_size.name() : __title_size,
        __text_size.name() : __text_size,
        __logo.name() : __logo,
        __background.name() : __background,
        __dummy_picture.name() : __dummy_picture,
        __hide_cursor.name() : __hide_cursor,
        __rotation.name() : __rotation,
        __email_form.name() : __email_form,
        __volume.name() : __volume
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Configuration = Configuration
Namespace.addCategoryObject('typeBinding', 'Configuration', Configuration)


# Complex type {http://xml.homeinfo.de/schema/presentation}Colors with content type ELEMENT_ONLY
class Colors (pyxb.binding.basis.complexTypeDefinition):
    """
                Farben der Konfiguration.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Colors')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 150, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element header uses Python identifier header
    __header = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'header'), 'header', '__httpxml_homeinfo_deschemapresentation_Colors_header', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 157, 12), )

    
    header = property(__header.value, __header.set, None, '\n                        Farbe der Kopfzeile.\n                    ')

    
    # Element header_background uses Python identifier header_background
    __header_background = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'header_background'), 'header_background', '__httpxml_homeinfo_deschemapresentation_Colors_header_background', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 164, 12), )

    
    header_background = property(__header_background.value, __header_background.set, None, '\n                        Hintergrundfarbe der Kopfzeile.\n                    ')

    
    # Element background_left uses Python identifier background_left
    __background_left = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'background_left'), 'background_left', '__httpxml_homeinfo_deschemapresentation_Colors_background_left', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 171, 12), )

    
    background_left = property(__background_left.value, __background_left.set, None, '\n                        Hintergrundfarbe links.\n                    ')

    
    # Element background_right uses Python identifier background_right
    __background_right = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'background_right'), 'background_right', '__httpxml_homeinfo_deschemapresentation_Colors_background_right', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 178, 12), )

    
    background_right = property(__background_right.value, __background_right.set, None, '\n                        Hintergrundfarbe rechts.\n                    ')

    
    # Element ticker uses Python identifier ticker
    __ticker = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ticker'), 'ticker', '__httpxml_homeinfo_deschemapresentation_Colors_ticker', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 185, 12), )

    
    ticker = property(__ticker.value, __ticker.set, None, '\n                        Farbe des Tickers.\n                    ')

    
    # Element ticker_background uses Python identifier ticker_background
    __ticker_background = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ticker_background'), 'ticker_background', '__httpxml_homeinfo_deschemapresentation_Colors_ticker_background', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 192, 12), )

    
    ticker_background = property(__ticker_background.value, __ticker_background.set, None, '\n                        Hintergrundfarbe des Tickers.\n                    ')

    
    # Element clock uses Python identifier clock
    __clock = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'clock'), 'clock', '__httpxml_homeinfo_deschemapresentation_Colors_clock', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 199, 12), )

    
    clock = property(__clock.value, __clock.set, None, '\n                        Farbe der Uhr.\n                    ')

    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__httpxml_homeinfo_deschemapresentation_Colors_title', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 206, 12), )

    
    title = property(__title.value, __title.set, None, '\n                        Farbe des Titels.\n                    ')

    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschemapresentation_Colors_text', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 213, 12), )

    
    text = property(__text.value, __text.set, None, '\n                        Textfarbe.\n                    ')

    
    # Element text_background uses Python identifier text_background
    __text_background = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text_background'), 'text_background', '__httpxml_homeinfo_deschemapresentation_Colors_text_background', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 220, 12), )

    
    text_background = property(__text_background.value, __text_background.set, None, '\n                        Hintergrundfarbe des Texts.\n                    ')

    _ElementMap.update({
        __header.name() : __header,
        __header_background.name() : __header_background,
        __background_left.name() : __background_left,
        __background_right.name() : __background_right,
        __ticker.name() : __ticker,
        __ticker_background.name() : __ticker_background,
        __clock.name() : __clock,
        __title.name() : __title,
        __text.name() : __text,
        __text_background.name() : __text_background
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Colors = Colors
Namespace.addCategoryObject('typeBinding', 'Colors', Colors)


# Complex type {http://xml.homeinfo.de/schema/presentation}Menu with content type ELEMENT_ONLY
class Menu (pyxb.binding.basis.complexTypeDefinition):
    """
                Ein Menü.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Menu')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 12, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpxml_homeinfo_deschemapresentation_Menu_name', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 19, 12), )

    
    name = property(__name.value, __name.set, None, '\n                        Name des Menüs.\n                    ')

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpxml_homeinfo_deschemapresentation_Menu_description', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 26, 12), )

    
    description = property(__description.value, __description.set, None, '\n                        Beschreibung des Menüs.\n                    ')

    
    # Element item uses Python identifier item
    __item = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'item'), 'item', '__httpxml_homeinfo_deschemapresentation_Menu_item', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 33, 12), )

    
    item = property(__item.value, __item.set, None, '\n                        Menüelemente.\n                    ')

    _ElementMap.update({
        __name.name() : __name,
        __description.name() : __description,
        __item.name() : __item
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Menu = Menu
Namespace.addCategoryObject('typeBinding', 'Menu', Menu)


# Complex type {http://xml.homeinfo.de/schema/presentation}MenuItem with content type ELEMENT_ONLY
class MenuItem (pyxb.binding.basis.complexTypeDefinition):
    """
                Menüelemente.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MenuItem')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 44, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpxml_homeinfo_deschemapresentation_MenuItem_name', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 51, 12), )

    
    name = property(__name.value, __name.set, None, '\n                        Name des Menüelements.\n                    ')

    
    # Element icon uses Python identifier icon
    __icon = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'icon'), 'icon', '__httpxml_homeinfo_deschemapresentation_MenuItem_icon', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 58, 12), )

    
    icon = property(__icon.value, __icon.set, None, '\n                        Symbol des Menüelements.\n                    ')

    
    # Element text_color uses Python identifier text_color
    __text_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text_color'), 'text_color', '__httpxml_homeinfo_deschemapresentation_MenuItem_text_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 65, 12), )

    
    text_color = property(__text_color.value, __text_color.set, None, '\n                        Schriftfarbe des Menüelements.\n                    ')

    
    # Element background_color uses Python identifier background_color
    __background_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'background_color'), 'background_color', '__httpxml_homeinfo_deschemapresentation_MenuItem_background_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 72, 12), )

    
    background_color = property(__background_color.value, __background_color.set, None, '\n                        Hintergrundfarbe des Menüelements.\n                    ')

    
    # Element index uses Python identifier index
    __index = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'index'), 'index', '__httpxml_homeinfo_deschemapresentation_MenuItem_index', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 79, 12), )

    
    index = property(__index.value, __index.set, None, '\n                        Position des Menüelements.\n                    ')

    
    # Element child uses Python identifier child
    __child = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'child'), 'child', '__httpxml_homeinfo_deschemapresentation_MenuItem_child', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 86, 12), )

    
    child = property(__child.value, __child.set, None, '\n                        Menüelemente.\n                    ')

    
    # Element chart uses Python identifier chart
    __chart = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'chart'), 'chart', '__httpxml_homeinfo_deschemapresentation_MenuItem_chart', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 93, 12), )

    
    chart = property(__chart.value, __chart.set, None, '\n                        Charts, welche diesem Menüelement zugeordnet sind.\n                    ')

    _ElementMap.update({
        __name.name() : __name,
        __icon.name() : __icon,
        __text_color.name() : __text_color,
        __background_color.name() : __background_color,
        __index.name() : __index,
        __child.name() : __child,
        __chart.name() : __chart
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MenuItem = MenuItem
Namespace.addCategoryObject('typeBinding', 'MenuItem', MenuItem)


# Complex type {http://xml.homeinfo.de/schema/presentation}MenuItemChart with content type ELEMENT_ONLY
class MenuItemChart (pyxb.binding.basis.complexTypeDefinition):
    """
                Chart eines Menüelements.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'MenuItemChart')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 104, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element chart_id uses Python identifier chart_id
    __chart_id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'chart_id'), 'chart_id', '__httpxml_homeinfo_deschemapresentation_MenuItemChart_chart_id', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 111, 12), )

    
    chart_id = property(__chart_id.value, __chart_id.set, None, '\n                        ID des entsprechenden Charts.\n                    ')

    
    # Element chart_type uses Python identifier chart_type
    __chart_type = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'chart_type'), 'chart_type', '__httpxml_homeinfo_deschemapresentation_MenuItemChart_chart_type', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 118, 12), )

    
    chart_type = property(__chart_type.value, __chart_type.set, None, '\n                        Der Typ des entsprechenden Charts.\n                    ')

    
    # Element index uses Python identifier index
    __index = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'index'), 'index', '__httpxml_homeinfo_deschemapresentation_MenuItemChart_index', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 125, 12), )

    
    index = property(__index.value, __index.set, None, '\n                        Position des Charts.\n                    ')

    _ElementMap.update({
        __chart_id.name() : __chart_id,
        __chart_type.name() : __chart_type,
        __index.name() : __index
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.MenuItemChart = MenuItemChart
Namespace.addCategoryObject('typeBinding', 'MenuItemChart', MenuItemChart)


# Complex type {http://xml.homeinfo.de/schema/presentation}FacebookAccount with content type ELEMENT_ONLY
class FacebookAccount (pyxb.binding.basis.complexTypeDefinition):
    """
                Ein Facebook Konto.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'FacebookAccount')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 12, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element facebook_id uses Python identifier facebook_id
    __facebook_id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'facebook_id'), 'facebook_id', '__httpxml_homeinfo_deschemapresentation_FacebookAccount_facebook_id', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 19, 12), )

    
    facebook_id = property(__facebook_id.value, __facebook_id.set, None, '\n                        Facebook ID.\n                    ')

    
    # Element recent_days uses Python identifier recent_days
    __recent_days = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'recent_days'), 'recent_days', '__httpxml_homeinfo_deschemapresentation_FacebookAccount_recent_days', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 26, 12), )

    
    recent_days = property(__recent_days.value, __recent_days.set, None, '\n                        Anzahl der letzten Tage.\n                    ')

    
    # Element max_posts uses Python identifier max_posts
    __max_posts = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'max_posts'), 'max_posts', '__httpxml_homeinfo_deschemapresentation_FacebookAccount_max_posts', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 33, 12), )

    
    max_posts = property(__max_posts.value, __max_posts.set, None, '\n                        Maximiale Anzahl an Posts.\n                    ')

    
    # Element name uses Python identifier name
    __name = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'name'), 'name', '__httpxml_homeinfo_deschemapresentation_FacebookAccount_name', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 40, 12), )

    
    name = property(__name.value, __name.set, None, '\n                        Name des Kontos.\n                    ')

    _ElementMap.update({
        __facebook_id.name() : __facebook_id,
        __recent_days.name() : __recent_days,
        __max_posts.name() : __max_posts,
        __name.name() : __name
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.FacebookAccount = FacebookAccount
Namespace.addCategoryObject('typeBinding', 'FacebookAccount', FacebookAccount)


# Complex type {http://xml.homeinfo.de/schema/presentation}Filter with content type EMPTY
class Filter (pyxb.binding.basis.complexTypeDefinition):
    """
                Ein Immobilien Filter.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_EMPTY
    _Abstract = True
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Filter')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 51, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Filter = Filter
Namespace.addCategoryObject('typeBinding', 'Filter', Filter)


# Complex type {http://xml.homeinfo.de/schema/presentation}Presentation with content type ELEMENT_ONLY
class Presentation (pyxb.binding.basis.complexTypeDefinition):
    """
                Hauptobjekt für Präsentationsdaten.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Presentation')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 26, 4)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element configuration uses Python identifier configuration
    __configuration = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'configuration'), 'configuration', '__httpxml_homeinfo_deschemapresentation_Presentation_configuration', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 33, 12), )

    
    configuration = property(__configuration.value, __configuration.set, None, '\n                        Konfigurationen.\n                    ')

    
    # Element menu uses Python identifier menu
    __menu = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'menu'), 'menu', '__httpxml_homeinfo_deschemapresentation_Presentation_menu', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 40, 12), )

    
    menu = property(__menu.value, __menu.set, None, '\n                        Menüs.\n                    ')

    
    # Element chart uses Python identifier chart
    __chart = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'chart'), 'chart', '__httpxml_homeinfo_deschemapresentation_Presentation_chart', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 47, 12), )

    
    chart = property(__chart.value, __chart.set, None, '\n                        Charts.\n                    ')

    
    # Attribute customer uses Python identifier customer
    __customer = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'customer'), 'customer', '__httpxml_homeinfo_deschemapresentation_Presentation_customer', pyxb.binding.datatypes.positiveInteger)
    __customer._DeclarationLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 55, 8)
    __customer._UseLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 55, 8)
    
    customer = property(__customer.value, __customer.set, None, '\n                    Die Kundennummer.\n                ')

    _ElementMap.update({
        __configuration.name() : __configuration,
        __menu.name() : __menu,
        __chart.name() : __chart
    })
    _AttributeMap.update({
        __customer.name() : __customer
    })
_module_typeBindings.Presentation = Presentation
Namespace.addCategoryObject('typeBinding', 'Presentation', Presentation)


# Complex type {http://xml.homeinfo.de/schema/presentation}Cleaning with content type ELEMENT_ONLY
class Cleaning (Chart):
    """
                Reinigungs Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Cleaning')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 107, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__httpxml_homeinfo_deschemapresentation_Cleaning_title', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 116, 20), )

    
    title = property(__title.value, __title.set, None, '\n                                Überschrift.\n                            ')

    
    # Element mode uses Python identifier mode
    __mode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mode'), 'mode', '__httpxml_homeinfo_deschemapresentation_Cleaning_mode', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 123, 20), )

    
    mode = property(__mode.value, __mode.set, None, '\n                                Modus des Charts.\n                            ')

    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschemapresentation_Cleaning_text', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 130, 20), )

    
    text = property(__text.value, __text.set, None, '\n                                Textinhalt.\n                            ')

    
    # Element font_size uses Python identifier font_size
    __font_size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_size'), 'font_size', '__httpxml_homeinfo_deschemapresentation_Cleaning_font_size', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 137, 20), )

    
    font_size = property(__font_size.value, __font_size.set, None, '\n                                Schriftgröße.\n                            ')

    
    # Element text_color uses Python identifier text_color
    __text_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text_color'), 'text_color', '__httpxml_homeinfo_deschemapresentation_Cleaning_text_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 144, 20), )

    
    text_color = property(__text_color.value, __text_color.set, None, '\n                                Textfarbe.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __title.name() : __title,
        __mode.name() : __mode,
        __text.name() : __text,
        __font_size.name() : __font_size,
        __text_color.name() : __text_color
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Cleaning = Cleaning
Namespace.addCategoryObject('typeBinding', 'Cleaning', Cleaning)


# Complex type {http://xml.homeinfo.de/schema/presentation}Facebook with content type ELEMENT_ONLY
class Facebook (Chart):
    """
                Facebook Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Facebook')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 157, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element font_size uses Python identifier font_size
    __font_size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_size'), 'font_size', '__httpxml_homeinfo_deschemapresentation_Facebook_font_size', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 166, 20), )

    
    font_size = property(__font_size.value, __font_size.set, None, '\n                                Schriftgröße.\n                            ')

    
    # Element title_color uses Python identifier title_color
    __title_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title_color'), 'title_color', '__httpxml_homeinfo_deschemapresentation_Facebook_title_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 173, 20), )

    
    title_color = property(__title_color.value, __title_color.set, None, '\n                                Textfarbe des Titels.\n                            ')

    
    # Element ken_burns uses Python identifier ken_burns
    __ken_burns = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ken_burns'), 'ken_burns', '__httpxml_homeinfo_deschemapresentation_Facebook_ken_burns', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 180, 20), )

    
    ken_burns = property(__ken_burns.value, __ken_burns.set, None, '\n                                Ken Burns Effekt.\n                            ')

    
    # Element account uses Python identifier account
    __account = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'account'), 'account', '__httpxml_homeinfo_deschemapresentation_Facebook_account', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 187, 20), )

    
    account = property(__account.value, __account.set, None, '\n                                Facebook Konten.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __font_size.name() : __font_size,
        __title_color.name() : __title_color,
        __ken_burns.name() : __ken_burns,
        __account.name() : __account
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Facebook = Facebook
Namespace.addCategoryObject('typeBinding', 'Facebook', Facebook)


# Complex type {http://xml.homeinfo.de/schema/presentation}Form with content type ELEMENT_ONLY
class Form (Chart):
    """
                Formular Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Form')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 200, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element mode uses Python identifier mode
    __mode = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'mode'), 'mode', '__httpxml_homeinfo_deschemapresentation_Form_mode', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 209, 20), )

    
    mode = property(__mode.value, __mode.set, None, '\n                                Typ (Modus) des Formulars.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __mode.name() : __mode
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Form = Form
Namespace.addCategoryObject('typeBinding', 'Form', Form)


# Complex type {http://xml.homeinfo.de/schema/presentation}GarbageCollection with content type ELEMENT_ONLY
class GarbageCollection (Chart):
    """
                Müllabfuhr Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GarbageCollection')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 222, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GarbageCollection = GarbageCollection
Namespace.addCategoryObject('typeBinding', 'GarbageCollection', GarbageCollection)


# Complex type {http://xml.homeinfo.de/schema/presentation}GuessPicture with content type ELEMENT_ONLY
class GuessPicture (Chart):
    """
                Bilderraten Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'GuessPicture')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 234, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.GuessPicture = GuessPicture
Namespace.addCategoryObject('typeBinding', 'GuessPicture', GuessPicture)


# Complex type {http://xml.homeinfo.de/schema/presentation}ImageText with content type ELEMENT_ONLY
class ImageText (Chart):
    """
                Bilderraten Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ImageText')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 246, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element style uses Python identifier style
    __style = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'style'), 'style', '__httpxml_homeinfo_deschemapresentation_ImageText_style', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 255, 20), )

    
    style = property(__style.value, __style.set, None, '\n                                Stil des Charts.\n                            ')

    
    # Element title uses Python identifier title
    __title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title'), 'title', '__httpxml_homeinfo_deschemapresentation_ImageText_title', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 262, 20), )

    
    title = property(__title.value, __title.set, None, '\n                                Titel des Charts.\n                            ')

    
    # Element font_size uses Python identifier font_size
    __font_size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_size'), 'font_size', '__httpxml_homeinfo_deschemapresentation_ImageText_font_size', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 269, 20), )

    
    font_size = property(__font_size.value, __font_size.set, None, '\n                                Schriftgröße.\n                            ')

    
    # Element title_color uses Python identifier title_color
    __title_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title_color'), 'title_color', '__httpxml_homeinfo_deschemapresentation_ImageText_title_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 276, 20), )

    
    title_color = property(__title_color.value, __title_color.set, None, '\n                                Titelfarbe.\n                            ')

    
    # Element ken_burns uses Python identifier ken_burns
    __ken_burns = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ken_burns'), 'ken_burns', '__httpxml_homeinfo_deschemapresentation_ImageText_ken_burns', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 283, 20), )

    
    ken_burns = property(__ken_burns.value, __ken_burns.set, None, '\n                                Ken Burns Effekt.\n                            ')

    
    # Element image uses Python identifier image
    __image = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'image'), 'image', '__httpxml_homeinfo_deschemapresentation_ImageText_image', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 290, 20), )

    
    image = property(__image.value, __image.set, None, '\n                                Bilder.\n                            ')

    
    # Element text uses Python identifier text
    __text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text'), 'text', '__httpxml_homeinfo_deschemapresentation_ImageText_text', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 297, 20), )

    
    text = property(__text.value, __text.set, None, '\n                                Texte.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __style.name() : __style,
        __title.name() : __title,
        __font_size.name() : __font_size,
        __title_color.name() : __title_color,
        __ken_burns.name() : __ken_burns,
        __image.name() : __image,
        __text.name() : __text
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ImageText = ImageText
Namespace.addCategoryObject('typeBinding', 'ImageText', ImageText)


# Complex type {http://xml.homeinfo.de/schema/presentation}News with content type ELEMENT_ONLY
class News (Chart):
    """
                Bilderraten Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'News')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 310, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element font_size_title uses Python identifier font_size_title
    __font_size_title = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_size_title'), 'font_size_title', '__httpxml_homeinfo_deschemapresentation_News_font_size_title', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 319, 20), )

    
    font_size_title = property(__font_size_title.value, __font_size_title.set, None, '\n                                Schriftgröße des Titles.\n                            ')

    
    # Element title_color uses Python identifier title_color
    __title_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'title_color'), 'title_color', '__httpxml_homeinfo_deschemapresentation_News_title_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 326, 20), )

    
    title_color = property(__title_color.value, __title_color.set, None, '\n                                Titelfarbe.\n                            ')

    
    # Element font_size_text uses Python identifier font_size_text
    __font_size_text = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_size_text'), 'font_size_text', '__httpxml_homeinfo_deschemapresentation_News_font_size_text', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 333, 20), )

    
    font_size_text = property(__font_size_text.value, __font_size_text.set, None, '\n                                Schriftgröße des Texts.\n                            ')

    
    # Element text_color uses Python identifier text_color
    __text_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'text_color'), 'text_color', '__httpxml_homeinfo_deschemapresentation_News_text_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 340, 20), )

    
    text_color = property(__text_color.value, __text_color.set, None, '\n                                Textfarbe.\n                            ')

    
    # Element ken_burns uses Python identifier ken_burns
    __ken_burns = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ken_burns'), 'ken_burns', '__httpxml_homeinfo_deschemapresentation_News_ken_burns', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 347, 20), )

    
    ken_burns = property(__ken_burns.value, __ken_burns.set, None, '\n                                Ken Burns Effekt.\n                            ')

    
    # Element news_token uses Python identifier news_token
    __news_token = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'news_token'), 'news_token', '__httpxml_homeinfo_deschemapresentation_News_news_token', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 354, 20), )

    
    news_token = property(__news_token.value, __news_token.set, None, '\n                                Token zur Abfrage von News.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __font_size_title.name() : __font_size_title,
        __title_color.name() : __title_color,
        __font_size_text.name() : __font_size_text,
        __text_color.name() : __text_color,
        __ken_burns.name() : __ken_burns,
        __news_token.name() : __news_token
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.News = News
Namespace.addCategoryObject('typeBinding', 'News', News)


# Complex type {http://xml.homeinfo.de/schema/presentation}PublicTransport with content type ELEMENT_ONLY
class PublicTransport (Chart):
    """
                ÖPNV Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'PublicTransport')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 367, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.PublicTransport = PublicTransport
Namespace.addCategoryObject('typeBinding', 'PublicTransport', PublicTransport)


# Complex type {http://xml.homeinfo.de/schema/presentation}Quotes with content type ELEMENT_ONLY
class Quotes (Chart):
    """
                Zitate Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Quotes')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 379, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element font_color uses Python identifier font_color
    __font_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_color'), 'font_color', '__httpxml_homeinfo_deschemapresentation_Quotes_font_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 388, 20), )

    
    font_color = property(__font_color.value, __font_color.set, None, '\n                                Schriftfarbe.\n                            ')

    
    # Element background_color uses Python identifier background_color
    __background_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'background_color'), 'background_color', '__httpxml_homeinfo_deschemapresentation_Quotes_background_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 395, 20), )

    
    background_color = property(__background_color.value, __background_color.set, None, '\n                                Hintergrundfarbe.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __font_color.name() : __font_color,
        __background_color.name() : __background_color
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Quotes = Quotes
Namespace.addCategoryObject('typeBinding', 'Quotes', Quotes)


# Complex type {http://xml.homeinfo.de/schema/presentation}RealEstates with content type ELEMENT_ONLY
class RealEstates (Chart):
    """
                Immobilien Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'RealEstates')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 408, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element display_format uses Python identifier display_format
    __display_format = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'display_format'), 'display_format', '__httpxml_homeinfo_deschemapresentation_RealEstates_display_format', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 417, 20), )

    
    display_format = property(__display_format.value, __display_format.set, None, '\n                                Anzeigeformat.\n                            ')

    
    # Element ken_burns uses Python identifier ken_burns
    __ken_burns = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'ken_burns'), 'ken_burns', '__httpxml_homeinfo_deschemapresentation_RealEstates_ken_burns', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 424, 20), )

    
    ken_burns = property(__ken_burns.value, __ken_burns.set, None, '\n                                Ken Burns Effekt.\n                            ')

    
    # Element scaling uses Python identifier scaling
    __scaling = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'scaling'), 'scaling', '__httpxml_homeinfo_deschemapresentation_RealEstates_scaling', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 431, 20), )

    
    scaling = property(__scaling.value, __scaling.set, None, '\n                                Soll die Application skalieren?\n                            ')

    
    # Element slideshow uses Python identifier slideshow
    __slideshow = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'slideshow'), 'slideshow', '__httpxml_homeinfo_deschemapresentation_RealEstates_slideshow', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 438, 20), )

    
    slideshow = property(__slideshow.value, __slideshow.set, None, '\n                                Soll die Application eine Slideshow anzeigen?\n                            ')

    
    # Element qr_codes uses Python identifier qr_codes
    __qr_codes = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'qr_codes'), 'qr_codes', '__httpxml_homeinfo_deschemapresentation_RealEstates_qr_codes', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 445, 20), )

    
    qr_codes = property(__qr_codes.value, __qr_codes.set, None, '\n                                Sollen QR Codes angezeigt werden?\n                            ')

    
    # Element show_contact uses Python identifier show_contact
    __show_contact = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'show_contact'), 'show_contact', '__httpxml_homeinfo_deschemapresentation_RealEstates_show_contact', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 452, 20), )

    
    show_contact = property(__show_contact.value, __show_contact.set, None, '\n                                Sollen Kontaktpersonen angezeigt werden?\n                            ')

    
    # Element contact_picture uses Python identifier contact_picture
    __contact_picture = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'contact_picture'), 'contact_picture', '__httpxml_homeinfo_deschemapresentation_RealEstates_contact_picture', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 459, 20), )

    
    contact_picture = property(__contact_picture.value, __contact_picture.set, None, '\n                                Sollen Bilder von Kontaktpersonen angezeigt werden?\n                            ')

    
    # Element font_size uses Python identifier font_size
    __font_size = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_size'), 'font_size', '__httpxml_homeinfo_deschemapresentation_RealEstates_font_size', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 466, 20), )

    
    font_size = property(__font_size.value, __font_size.set, None, '\n                                Schriftgröße.\n                            ')

    
    # Element font_color uses Python identifier font_color
    __font_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_color'), 'font_color', '__httpxml_homeinfo_deschemapresentation_RealEstates_font_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 473, 20), )

    
    font_color = property(__font_color.value, __font_color.set, None, '\n                                Schriftfarbe.\n                            ')

    
    # Element amenities uses Python identifier amenities
    __amenities = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'amenities'), 'amenities', '__httpxml_homeinfo_deschemapresentation_RealEstates_amenities', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 481, 20), )

    
    amenities = property(__amenities.value, __amenities.set, None, None)

    
    # Element construction uses Python identifier construction
    __construction = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'construction'), 'construction', '__httpxml_homeinfo_deschemapresentation_RealEstates_construction', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 482, 20), )

    
    construction = property(__construction.value, __construction.set, None, None)

    
    # Element courtage uses Python identifier courtage
    __courtage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'courtage'), 'courtage', '__httpxml_homeinfo_deschemapresentation_RealEstates_courtage', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 483, 20), )

    
    courtage = property(__courtage.value, __courtage.set, None, None)

    
    # Element floor uses Python identifier floor
    __floor = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'floor'), 'floor', '__httpxml_homeinfo_deschemapresentation_RealEstates_floor', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 484, 20), )

    
    floor = property(__floor.value, __floor.set, None, None)

    
    # Element area uses Python identifier area
    __area = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'area'), 'area', '__httpxml_homeinfo_deschemapresentation_RealEstates_area', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 485, 20), )

    
    area = property(__area.value, __area.set, None, None)

    
    # Element free_from uses Python identifier free_from
    __free_from = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'free_from'), 'free_from', '__httpxml_homeinfo_deschemapresentation_RealEstates_free_from', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 486, 20), )

    
    free_from = property(__free_from.value, __free_from.set, None, None)

    
    # Element coop_share uses Python identifier coop_share
    __coop_share = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'coop_share'), 'coop_share', '__httpxml_homeinfo_deschemapresentation_RealEstates_coop_share', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 487, 20), )

    
    coop_share = property(__coop_share.value, __coop_share.set, None, None)

    
    # Element total_area uses Python identifier total_area
    __total_area = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'total_area'), 'total_area', '__httpxml_homeinfo_deschemapresentation_RealEstates_total_area', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 488, 20), )

    
    total_area = property(__total_area.value, __total_area.set, None, None)

    
    # Element plot_area uses Python identifier plot_area
    __plot_area = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'plot_area'), 'plot_area', '__httpxml_homeinfo_deschemapresentation_RealEstates_plot_area', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 489, 20), )

    
    plot_area = property(__plot_area.value, __plot_area.set, None, None)

    
    # Element cold_rent uses Python identifier cold_rent
    __cold_rent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cold_rent'), 'cold_rent', '__httpxml_homeinfo_deschemapresentation_RealEstates_cold_rent', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 490, 20), )

    
    cold_rent = property(__cold_rent.value, __cold_rent.set, None, None)

    
    # Element purchase_price uses Python identifier purchase_price
    __purchase_price = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'purchase_price'), 'purchase_price', '__httpxml_homeinfo_deschemapresentation_RealEstates_purchase_price', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 491, 20), )

    
    purchase_price = property(__purchase_price.value, __purchase_price.set, None, None)

    
    # Element security_deposit uses Python identifier security_deposit
    __security_deposit = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'security_deposit'), 'security_deposit', '__httpxml_homeinfo_deschemapresentation_RealEstates_security_deposit', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 492, 20), )

    
    security_deposit = property(__security_deposit.value, __security_deposit.set, None, None)

    
    # Element service_charge uses Python identifier service_charge
    __service_charge = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'service_charge'), 'service_charge', '__httpxml_homeinfo_deschemapresentation_RealEstates_service_charge', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 493, 20), )

    
    service_charge = property(__service_charge.value, __service_charge.set, None, None)

    
    # Element object_id uses Python identifier object_id
    __object_id = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'object_id'), 'object_id', '__httpxml_homeinfo_deschemapresentation_RealEstates_object_id', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 494, 20), )

    
    object_id = property(__object_id.value, __object_id.set, None, None)

    
    # Element description uses Python identifier description
    __description = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'description'), 'description', '__httpxml_homeinfo_deschemapresentation_RealEstates_description', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 495, 20), )

    
    description = property(__description.value, __description.set, None, None)

    
    # Element warm_rent uses Python identifier warm_rent
    __warm_rent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'warm_rent'), 'warm_rent', '__httpxml_homeinfo_deschemapresentation_RealEstates_warm_rent', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 496, 20), )

    
    warm_rent = property(__warm_rent.value, __warm_rent.set, None, None)

    
    # Element rooms uses Python identifier rooms
    __rooms = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms'), 'rooms', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 497, 20), )

    
    rooms = property(__rooms.value, __rooms.set, None, None)

    
    # Element lift uses Python identifier lift
    __lift = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lift'), 'lift', '__httpxml_homeinfo_deschemapresentation_RealEstates_lift', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 499, 20), )

    
    lift = property(__lift.value, __lift.set, None, None)

    
    # Element bathtub uses Python identifier bathtub
    __bathtub = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'bathtub'), 'bathtub', '__httpxml_homeinfo_deschemapresentation_RealEstates_bathtub', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 500, 20), )

    
    bathtub = property(__bathtub.value, __bathtub.set, None, None)

    
    # Element balcony uses Python identifier balcony
    __balcony = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'balcony'), 'balcony', '__httpxml_homeinfo_deschemapresentation_RealEstates_balcony', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 501, 20), )

    
    balcony = property(__balcony.value, __balcony.set, None, None)

    
    # Element accessibility uses Python identifier accessibility
    __accessibility = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'accessibility'), 'accessibility', '__httpxml_homeinfo_deschemapresentation_RealEstates_accessibility', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 502, 20), )

    
    accessibility = property(__accessibility.value, __accessibility.set, None, None)

    
    # Element assited_living uses Python identifier assited_living
    __assited_living = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'assited_living'), 'assited_living', '__httpxml_homeinfo_deschemapresentation_RealEstates_assited_living', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 503, 20), )

    
    assited_living = property(__assited_living.value, __assited_living.set, None, None)

    
    # Element carport uses Python identifier carport
    __carport = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'carport'), 'carport', '__httpxml_homeinfo_deschemapresentation_RealEstates_carport', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 504, 20), )

    
    carport = property(__carport.value, __carport.set, None, None)

    
    # Element floorboards uses Python identifier floorboards
    __floorboards = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'floorboards'), 'floorboards', '__httpxml_homeinfo_deschemapresentation_RealEstates_floorboards', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 505, 20), )

    
    floorboards = property(__floorboards.value, __floorboards.set, None, None)

    
    # Element duplex uses Python identifier duplex
    __duplex = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'duplex'), 'duplex', '__httpxml_homeinfo_deschemapresentation_RealEstates_duplex', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 506, 20), )

    
    duplex = property(__duplex.value, __duplex.set, None, None)

    
    # Element shower uses Python identifier shower
    __shower = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'shower'), 'shower', '__httpxml_homeinfo_deschemapresentation_RealEstates_shower', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 507, 20), )

    
    shower = property(__shower.value, __shower.set, None, None)

    
    # Element builtin_kitchen uses Python identifier builtin_kitchen
    __builtin_kitchen = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'builtin_kitchen'), 'builtin_kitchen', '__httpxml_homeinfo_deschemapresentation_RealEstates_builtin_kitchen', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 508, 20), )

    
    builtin_kitchen = property(__builtin_kitchen.value, __builtin_kitchen.set, None, None)

    
    # Element screed uses Python identifier screed
    __screed = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'screed'), 'screed', '__httpxml_homeinfo_deschemapresentation_RealEstates_screed', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 509, 20), )

    
    screed = property(__screed.value, __screed.set, None, None)

    
    # Element tiles uses Python identifier tiles
    __tiles = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'tiles'), 'tiles', '__httpxml_homeinfo_deschemapresentation_RealEstates_tiles', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 510, 20), )

    
    tiles = property(__tiles.value, __tiles.set, None, None)

    
    # Element outdoor_parking uses Python identifier outdoor_parking
    __outdoor_parking = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'outdoor_parking'), 'outdoor_parking', '__httpxml_homeinfo_deschemapresentation_RealEstates_outdoor_parking', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 511, 20), )

    
    outdoor_parking = property(__outdoor_parking.value, __outdoor_parking.set, None, None)

    
    # Element garage uses Python identifier garage
    __garage = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'garage'), 'garage', '__httpxml_homeinfo_deschemapresentation_RealEstates_garage', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 512, 20), )

    
    garage = property(__garage.value, __garage.set, None, None)

    
    # Element cable_sat_tv uses Python identifier cable_sat_tv
    __cable_sat_tv = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'cable_sat_tv'), 'cable_sat_tv', '__httpxml_homeinfo_deschemapresentation_RealEstates_cable_sat_tv', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 513, 20), )

    
    cable_sat_tv = property(__cable_sat_tv.value, __cable_sat_tv.set, None, None)

    
    # Element fireplace uses Python identifier fireplace
    __fireplace = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'fireplace'), 'fireplace', '__httpxml_homeinfo_deschemapresentation_RealEstates_fireplace', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 514, 20), )

    
    fireplace = property(__fireplace.value, __fireplace.set, None, None)

    
    # Element basement uses Python identifier basement
    __basement = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'basement'), 'basement', '__httpxml_homeinfo_deschemapresentation_RealEstates_basement', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 515, 20), )

    
    basement = property(__basement.value, __basement.set, None, None)

    
    # Element plastic uses Python identifier plastic
    __plastic = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'plastic'), 'plastic', '__httpxml_homeinfo_deschemapresentation_RealEstates_plastic', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 516, 20), )

    
    plastic = property(__plastic.value, __plastic.set, None, None)

    
    # Element furnished uses Python identifier furnished
    __furnished = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'furnished'), 'furnished', '__httpxml_homeinfo_deschemapresentation_RealEstates_furnished', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 517, 20), )

    
    furnished = property(__furnished.value, __furnished.set, None, None)

    
    # Element parquet uses Python identifier parquet
    __parquet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'parquet'), 'parquet', '__httpxml_homeinfo_deschemapresentation_RealEstates_parquet', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 518, 20), )

    
    parquet = property(__parquet.value, __parquet.set, None, None)

    
    # Element car_park uses Python identifier car_park
    __car_park = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'car_park'), 'car_park', '__httpxml_homeinfo_deschemapresentation_RealEstates_car_park', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 519, 20), )

    
    car_park = property(__car_park.value, __car_park.set, None, None)

    
    # Element wheelchair_accessible uses Python identifier wheelchair_accessible
    __wheelchair_accessible = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'wheelchair_accessible'), 'wheelchair_accessible', '__httpxml_homeinfo_deschemapresentation_RealEstates_wheelchair_accessible', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 520, 20), )

    
    wheelchair_accessible = property(__wheelchair_accessible.value, __wheelchair_accessible.set, None, None)

    
    # Element sauna uses Python identifier sauna
    __sauna = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'sauna'), 'sauna', '__httpxml_homeinfo_deschemapresentation_RealEstates_sauna', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 521, 20), )

    
    sauna = property(__sauna.value, __sauna.set, None, None)

    
    # Element stone uses Python identifier stone
    __stone = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'stone'), 'stone', '__httpxml_homeinfo_deschemapresentation_RealEstates_stone', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 522, 20), )

    
    stone = property(__stone.value, __stone.set, None, None)

    
    # Element swimming_pool uses Python identifier swimming_pool
    __swimming_pool = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'swimming_pool'), 'swimming_pool', '__httpxml_homeinfo_deschemapresentation_RealEstates_swimming_pool', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 523, 20), )

    
    swimming_pool = property(__swimming_pool.value, __swimming_pool.set, None, None)

    
    # Element carpet uses Python identifier carpet
    __carpet = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'carpet'), 'carpet', '__httpxml_homeinfo_deschemapresentation_RealEstates_carpet', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 524, 20), )

    
    carpet = property(__carpet.value, __carpet.set, None, None)

    
    # Element underground_carpark uses Python identifier underground_carpark
    __underground_carpark = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'underground_carpark'), 'underground_carpark', '__httpxml_homeinfo_deschemapresentation_RealEstates_underground_carpark', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 525, 20), )

    
    underground_carpark = property(__underground_carpark.value, __underground_carpark.set, None, None)

    
    # Element lavatory uses Python identifier lavatory
    __lavatory = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'lavatory'), 'lavatory', '__httpxml_homeinfo_deschemapresentation_RealEstates_lavatory', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 526, 20), )

    
    lavatory = property(__lavatory.value, __lavatory.set, None, None)

    
    # Element rooms_1 uses Python identifier rooms_1
    __rooms_1 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms_1'), 'rooms_1', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms_1', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 528, 20), )

    
    rooms_1 = property(__rooms_1.value, __rooms_1.set, None, None)

    
    # Element rooms_2 uses Python identifier rooms_2
    __rooms_2 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms_2'), 'rooms_2', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms_2', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 529, 20), )

    
    rooms_2 = property(__rooms_2.value, __rooms_2.set, None, None)

    
    # Element rooms_3 uses Python identifier rooms_3
    __rooms_3 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms_3'), 'rooms_3', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms_3', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 530, 20), )

    
    rooms_3 = property(__rooms_3.value, __rooms_3.set, None, None)

    
    # Element rooms_4 uses Python identifier rooms_4
    __rooms_4 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms_4'), 'rooms_4', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms_4', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 531, 20), )

    
    rooms_4 = property(__rooms_4.value, __rooms_4.set, None, None)

    
    # Element rooms_5 uses Python identifier rooms_5
    __rooms_5 = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms_5'), 'rooms_5', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms_5', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 532, 20), )

    
    rooms_5 = property(__rooms_5.value, __rooms_5.set, None, None)

    
    # Element rooms_5_or_more uses Python identifier rooms_5_or_more
    __rooms_5_or_more = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rooms_5_or_more'), 'rooms_5_or_more', '__httpxml_homeinfo_deschemapresentation_RealEstates_rooms_5_or_more', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 533, 20), )

    
    rooms_5_or_more = property(__rooms_5_or_more.value, __rooms_5_or_more.set, None, None)

    
    # Element finance_project uses Python identifier finance_project
    __finance_project = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'finance_project'), 'finance_project', '__httpxml_homeinfo_deschemapresentation_RealEstates_finance_project', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 535, 20), )

    
    finance_project = property(__finance_project.value, __finance_project.set, None, None)

    
    # Element business_realty uses Python identifier business_realty
    __business_realty = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'business_realty'), 'business_realty', '__httpxml_homeinfo_deschemapresentation_RealEstates_business_realty', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 536, 20), )

    
    business_realty = property(__business_realty.value, __business_realty.set, None, None)

    
    # Element short_term_accommocation uses Python identifier short_term_accommocation
    __short_term_accommocation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'short_term_accommocation'), 'short_term_accommocation', '__httpxml_homeinfo_deschemapresentation_RealEstates_short_term_accommocation', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 537, 20), )

    
    short_term_accommocation = property(__short_term_accommocation.value, __short_term_accommocation.set, None, None)

    
    # Element living_realty uses Python identifier living_realty
    __living_realty = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'living_realty'), 'living_realty', '__httpxml_homeinfo_deschemapresentation_RealEstates_living_realty', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 538, 20), )

    
    living_realty = property(__living_realty.value, __living_realty.set, None, None)

    
    # Element office uses Python identifier office
    __office = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'office'), 'office', '__httpxml_homeinfo_deschemapresentation_RealEstates_office', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 540, 20), )

    
    office = property(__office.value, __office.set, None, None)

    
    # Element retail uses Python identifier retail
    __retail = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'retail'), 'retail', '__httpxml_homeinfo_deschemapresentation_RealEstates_retail', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 541, 20), )

    
    retail = property(__retail.value, __retail.set, None, None)

    
    # Element recreational uses Python identifier recreational
    __recreational = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'recreational'), 'recreational', '__httpxml_homeinfo_deschemapresentation_RealEstates_recreational', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 542, 20), )

    
    recreational = property(__recreational.value, __recreational.set, None, None)

    
    # Element hospitality_industry uses Python identifier hospitality_industry
    __hospitality_industry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hospitality_industry'), 'hospitality_industry', '__httpxml_homeinfo_deschemapresentation_RealEstates_hospitality_industry', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 543, 20), )

    
    hospitality_industry = property(__hospitality_industry.value, __hospitality_industry.set, None, None)

    
    # Element plot uses Python identifier plot
    __plot = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'plot'), 'plot', '__httpxml_homeinfo_deschemapresentation_RealEstates_plot', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 544, 20), )

    
    plot = property(__plot.value, __plot.set, None, None)

    
    # Element hall_warehouse_production uses Python identifier hall_warehouse_production
    __hall_warehouse_production = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'hall_warehouse_production'), 'hall_warehouse_production', '__httpxml_homeinfo_deschemapresentation_RealEstates_hall_warehouse_production', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 545, 20), )

    
    hall_warehouse_production = property(__hall_warehouse_production.value, __hall_warehouse_production.set, None, None)

    
    # Element house uses Python identifier house
    __house = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'house'), 'house', '__httpxml_homeinfo_deschemapresentation_RealEstates_house', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 546, 20), )

    
    house = property(__house.value, __house.set, None, None)

    
    # Element agriculture_forestry uses Python identifier agriculture_forestry
    __agriculture_forestry = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'agriculture_forestry'), 'agriculture_forestry', '__httpxml_homeinfo_deschemapresentation_RealEstates_agriculture_forestry', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 547, 20), )

    
    agriculture_forestry = property(__agriculture_forestry.value, __agriculture_forestry.set, None, None)

    
    # Element miscellaneous uses Python identifier miscellaneous
    __miscellaneous = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'miscellaneous'), 'miscellaneous', '__httpxml_homeinfo_deschemapresentation_RealEstates_miscellaneous', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 548, 20), )

    
    miscellaneous = property(__miscellaneous.value, __miscellaneous.set, None, None)

    
    # Element flat uses Python identifier flat
    __flat = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'flat'), 'flat', '__httpxml_homeinfo_deschemapresentation_RealEstates_flat', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 549, 20), )

    
    flat = property(__flat.value, __flat.set, None, None)

    
    # Element room uses Python identifier room
    __room = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'room'), 'room', '__httpxml_homeinfo_deschemapresentation_RealEstates_room', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 550, 20), )

    
    room = property(__room.value, __room.set, None, None)

    
    # Element income_property uses Python identifier income_property
    __income_property = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'income_property'), 'income_property', '__httpxml_homeinfo_deschemapresentation_RealEstates_income_property', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 551, 20), )

    
    income_property = property(__income_property.value, __income_property.set, None, None)

    
    # Element emphyteusis uses Python identifier emphyteusis
    __emphyteusis = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'emphyteusis'), 'emphyteusis', '__httpxml_homeinfo_deschemapresentation_RealEstates_emphyteusis', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 553, 20), )

    
    emphyteusis = property(__emphyteusis.value, __emphyteusis.set, None, None)

    
    # Element leasing uses Python identifier leasing
    __leasing = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'leasing'), 'leasing', '__httpxml_homeinfo_deschemapresentation_RealEstates_leasing', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 554, 20), )

    
    leasing = property(__leasing.value, __leasing.set, None, None)

    
    # Element rent uses Python identifier rent
    __rent = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'rent'), 'rent', '__httpxml_homeinfo_deschemapresentation_RealEstates_rent', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 555, 20), )

    
    rent = property(__rent.value, __rent.set, None, None)

    
    # Element sale uses Python identifier sale
    __sale = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'sale'), 'sale', '__httpxml_homeinfo_deschemapresentation_RealEstates_sale', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 556, 20), )

    
    sale = property(__sale.value, __sale.set, None, None)

    
    # Element filter uses Python identifier filter
    __filter = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'filter'), 'filter', '__httpxml_homeinfo_deschemapresentation_RealEstates_filter', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 558, 20), )

    
    filter = property(__filter.value, __filter.set, None, None)

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __display_format.name() : __display_format,
        __ken_burns.name() : __ken_burns,
        __scaling.name() : __scaling,
        __slideshow.name() : __slideshow,
        __qr_codes.name() : __qr_codes,
        __show_contact.name() : __show_contact,
        __contact_picture.name() : __contact_picture,
        __font_size.name() : __font_size,
        __font_color.name() : __font_color,
        __amenities.name() : __amenities,
        __construction.name() : __construction,
        __courtage.name() : __courtage,
        __floor.name() : __floor,
        __area.name() : __area,
        __free_from.name() : __free_from,
        __coop_share.name() : __coop_share,
        __total_area.name() : __total_area,
        __plot_area.name() : __plot_area,
        __cold_rent.name() : __cold_rent,
        __purchase_price.name() : __purchase_price,
        __security_deposit.name() : __security_deposit,
        __service_charge.name() : __service_charge,
        __object_id.name() : __object_id,
        __description.name() : __description,
        __warm_rent.name() : __warm_rent,
        __rooms.name() : __rooms,
        __lift.name() : __lift,
        __bathtub.name() : __bathtub,
        __balcony.name() : __balcony,
        __accessibility.name() : __accessibility,
        __assited_living.name() : __assited_living,
        __carport.name() : __carport,
        __floorboards.name() : __floorboards,
        __duplex.name() : __duplex,
        __shower.name() : __shower,
        __builtin_kitchen.name() : __builtin_kitchen,
        __screed.name() : __screed,
        __tiles.name() : __tiles,
        __outdoor_parking.name() : __outdoor_parking,
        __garage.name() : __garage,
        __cable_sat_tv.name() : __cable_sat_tv,
        __fireplace.name() : __fireplace,
        __basement.name() : __basement,
        __plastic.name() : __plastic,
        __furnished.name() : __furnished,
        __parquet.name() : __parquet,
        __car_park.name() : __car_park,
        __wheelchair_accessible.name() : __wheelchair_accessible,
        __sauna.name() : __sauna,
        __stone.name() : __stone,
        __swimming_pool.name() : __swimming_pool,
        __carpet.name() : __carpet,
        __underground_carpark.name() : __underground_carpark,
        __lavatory.name() : __lavatory,
        __rooms_1.name() : __rooms_1,
        __rooms_2.name() : __rooms_2,
        __rooms_3.name() : __rooms_3,
        __rooms_4.name() : __rooms_4,
        __rooms_5.name() : __rooms_5,
        __rooms_5_or_more.name() : __rooms_5_or_more,
        __finance_project.name() : __finance_project,
        __business_realty.name() : __business_realty,
        __short_term_accommocation.name() : __short_term_accommocation,
        __living_realty.name() : __living_realty,
        __office.name() : __office,
        __retail.name() : __retail,
        __recreational.name() : __recreational,
        __hospitality_industry.name() : __hospitality_industry,
        __plot.name() : __plot,
        __hall_warehouse_production.name() : __hall_warehouse_production,
        __house.name() : __house,
        __agriculture_forestry.name() : __agriculture_forestry,
        __miscellaneous.name() : __miscellaneous,
        __flat.name() : __flat,
        __room.name() : __room,
        __income_property.name() : __income_property,
        __emphyteusis.name() : __emphyteusis,
        __leasing.name() : __leasing,
        __rent.name() : __rent,
        __sale.name() : __sale,
        __filter.name() : __filter
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.RealEstates = RealEstates
Namespace.addCategoryObject('typeBinding', 'RealEstates', RealEstates)


# Complex type {http://xml.homeinfo.de/schema/presentation}Video with content type ELEMENT_ONLY
class Video (Chart):
    """
                Video Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Video')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 565, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element video uses Python identifier video
    __video = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'video'), 'video', '__httpxml_homeinfo_deschemapresentation_Video_video', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 574, 20), )

    
    video = property(__video.value, __video.set, None, '\n                                Das entsprechende Video.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __video.name() : __video
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Video = Video
Namespace.addCategoryObject('typeBinding', 'Video', Video)


# Complex type {http://xml.homeinfo.de/schema/presentation}Weather with content type ELEMENT_ONLY
class Weather (Chart):
    """
                Wetter Chart.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Weather')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 587, 4)
    _ElementMap = Chart._ElementMap.copy()
    _AttributeMap = Chart._AttributeMap.copy()
    # Base type is Chart
    
    # Element base (base) inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Element location uses Python identifier location
    __location = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'location'), 'location', '__httpxml_homeinfo_deschemapresentation_Weather_location', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 596, 20), )

    
    location = property(__location.value, __location.set, None, '\n                                Ort des Wetters.\n                            ')

    
    # Element font_color uses Python identifier font_color
    __font_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'font_color'), 'font_color', '__httpxml_homeinfo_deschemapresentation_Weather_font_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 603, 20), )

    
    font_color = property(__font_color.value, __font_color.set, None, '\n                                Schriftfarbe.\n                            ')

    
    # Element icon_color uses Python identifier icon_color
    __icon_color = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'icon_color'), 'icon_color', '__httpxml_homeinfo_deschemapresentation_Weather_icon_color', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 610, 20), )

    
    icon_color = property(__icon_color.value, __icon_color.set, None, '\n                                Icon Farbe.\n                            ')

    
    # Element box_color_top uses Python identifier box_color_top
    __box_color_top = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'box_color_top'), 'box_color_top', '__httpxml_homeinfo_deschemapresentation_Weather_box_color_top', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 617, 20), )

    
    box_color_top = property(__box_color_top.value, __box_color_top.set, None, '\n                                Obere Farbe der Box.\n                            ')

    
    # Element box_color_middle uses Python identifier box_color_middle
    __box_color_middle = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'box_color_middle'), 'box_color_middle', '__httpxml_homeinfo_deschemapresentation_Weather_box_color_middle', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 624, 20), )

    
    box_color_middle = property(__box_color_middle.value, __box_color_middle.set, None, '\n                                Mittlere Farbe der Box.\n                            ')

    
    # Element box_color_bottom uses Python identifier box_color_bottom
    __box_color_bottom = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'box_color_bottom'), 'box_color_bottom', '__httpxml_homeinfo_deschemapresentation_Weather_box_color_bottom', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 631, 20), )

    
    box_color_bottom = property(__box_color_bottom.value, __box_color_bottom.set, None, '\n                                Untere Farbe der Box.\n                            ')

    
    # Element transparency uses Python identifier transparency
    __transparency = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'transparency'), 'transparency', '__httpxml_homeinfo_deschemapresentation_Weather_transparency', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 638, 20), )

    
    transparency = property(__transparency.value, __transparency.set, None, '\n                                Transparenz.\n                            ')

    
    # Element image uses Python identifier image
    __image = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'image'), 'image', '__httpxml_homeinfo_deschemapresentation_Weather_image', True, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 645, 20), )

    
    image = property(__image.value, __image.set, None, '\n                                Bilder.\n                            ')

    
    # Attribute id inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    
    # Attribute type inherited from {http://xml.homeinfo.de/schema/presentation}Chart
    _ElementMap.update({
        __location.name() : __location,
        __font_color.name() : __font_color,
        __icon_color.name() : __icon_color,
        __box_color_top.name() : __box_color_top,
        __box_color_middle.name() : __box_color_middle,
        __box_color_bottom.name() : __box_color_bottom,
        __transparency.name() : __transparency,
        __image.name() : __image
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.Weather = Weather
Namespace.addCategoryObject('typeBinding', 'Weather', Weather)


# Complex type {http://xml.homeinfo.de/schema/presentation}IdFilter with content type ELEMENT_ONLY
class IdFilter (Filter):
    """
                Ein Immobilien Filter zur Filterung nach IDs.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'IdFilter')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 60, 4)
    _ElementMap = Filter._ElementMap.copy()
    _AttributeMap = Filter._AttributeMap.copy()
    # Base type is Filter
    
    # Element value uses Python identifier value_
    __value = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'value'), 'value_', '__httpxml_homeinfo_deschemapresentation_IdFilter_value', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 69, 20), )

    
    value_ = property(__value.value, __value.set, None, '\n                                Wert der ID.\n                            ')

    
    # Element type uses Python identifier type
    __type = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'type'), 'type', '__httpxml_homeinfo_deschemapresentation_IdFilter_type', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 76, 20), )

    
    type = property(__type.value, __type.set, None, '\n                                Typ der ID.\n                            ')

    _ElementMap.update({
        __value.name() : __value,
        __type.name() : __type
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.IdFilter = IdFilter
Namespace.addCategoryObject('typeBinding', 'IdFilter', IdFilter)


# Complex type {http://xml.homeinfo.de/schema/presentation}ZipCodeFilter with content type ELEMENT_ONLY
class ZipCodeFilter (Filter):
    """
                Ein Immobilien Filter zur Filterung nach IDs.
            """
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'ZipCodeFilter')
    _XSDLocation = pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 89, 4)
    _ElementMap = Filter._ElementMap.copy()
    _AttributeMap = Filter._AttributeMap.copy()
    # Base type is Filter
    
    # Element zip_code uses Python identifier zip_code
    __zip_code = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'zip_code'), 'zip_code', '__httpxml_homeinfo_deschemapresentation_ZipCodeFilter_zip_code', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 98, 20), )

    
    zip_code = property(__zip_code.value, __zip_code.set, None, '\n                                Postleitzahl.\n                            ')

    
    # Element blacklist uses Python identifier blacklist
    __blacklist = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(None, 'blacklist'), 'blacklist', '__httpxml_homeinfo_deschemapresentation_ZipCodeFilter_blacklist', False, pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 105, 20), )

    
    blacklist = property(__blacklist.value, __blacklist.set, None, '\n                                Handelt es sich um eine Blacklist (true) oder Whitelist(false)?\n                            ')

    _ElementMap.update({
        __zip_code.name() : __zip_code,
        __blacklist.name() : __blacklist
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.ZipCodeFilter = ZipCodeFilter
Namespace.addCategoryObject('typeBinding', 'ZipCodeFilter', ZipCodeFilter)


presentation = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'presentation'), Presentation, documentation='\n                Wurzelelement.\n            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 17, 4))
Namespace.addCategoryObject('elementBinding', presentation.name().localName(), presentation)



Attachment._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mimetype'), pyxb.binding.datatypes.string, scope=Attachment, documentation='\n                        MIME Typ.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 19, 12)))

Attachment._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'filename'), pyxb.binding.datatypes.string, scope=Attachment, documentation='\n                        Dateiname.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 26, 12)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Attachment._UseForTag(pyxb.namespace.ExpandedName(None, 'mimetype')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 19, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Attachment._UseForTag(pyxb.namespace.ExpandedName(None, 'filename')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/attachments.xsd', 26, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Attachment._Automaton = _BuildAutomaton()




BaseChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), pyxb.binding.datatypes.string, scope=BaseChart, documentation='\n                        Der Titel des Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 22, 12)))

BaseChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.string, scope=BaseChart, documentation='\n                        Die Beschreibung des Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 29, 12)))

BaseChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'duration'), pyxb.binding.datatypes.unsignedShort, scope=BaseChart, documentation='\n                        Die Anzeigedauer des Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 36, 12)))

BaseChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'transition'), pyxb.binding.datatypes.string, scope=BaseChart, documentation='\n                        Übergangseffekt.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 43, 12)))

BaseChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'created'), pyxb.binding.datatypes.dateTime, scope=BaseChart, documentation='\n                        Datum der Erstellung.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 50, 12)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 29, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BaseChart._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 22, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BaseChart._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 29, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BaseChart._UseForTag(pyxb.namespace.ExpandedName(None, 'duration')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 36, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(BaseChart._UseForTag(pyxb.namespace.ExpandedName(None, 'transition')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 43, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(BaseChart._UseForTag(pyxb.namespace.ExpandedName(None, 'created')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 50, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
BaseChart._Automaton = _BuildAutomaton_()




Chart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'base'), BaseChart, scope=Chart, documentation='\n                        Der zugehörige Basis-Chart.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Chart._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Chart._Automaton = _BuildAutomaton_2()




Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), pyxb.binding.datatypes.string, scope=Configuration, documentation='\n                        Name der Konfiguration.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 20, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.string, scope=Configuration, documentation='\n                        Beschreibung der Konfiguration.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 27, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font'), pyxb.binding.datatypes.string, scope=Configuration, documentation='\n                        Schriftart.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 34, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'portrait'), pyxb.binding.datatypes.boolean, scope=Configuration, documentation='\n                        Soll Portrait Darstellung verwendet werden?\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 41, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'touch'), pyxb.binding.datatypes.boolean, scope=Configuration, documentation='\n                        Handelt es sich um ein Touch System?\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 48, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'design'), pyxb.binding.datatypes.string, scope=Configuration, documentation='\n                        Das verwendete Design.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 55, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'effects'), pyxb.binding.datatypes.boolean, scope=Configuration, documentation='\n                        Sollen Effekte verwendet werden?\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 62, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ticker_speed'), pyxb.binding.datatypes.unsignedShort, scope=Configuration, documentation='\n                        Geschwindigkeit des Tickers.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 69, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'colors'), Colors, scope=Configuration, documentation='\n                        Die verwendeten Farben.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 76, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title_size'), pyxb.binding.datatypes.unsignedShort, scope=Configuration, documentation='\n                        Größe des Titels.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 83, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text_size'), pyxb.binding.datatypes.unsignedShort, scope=Configuration, documentation='\n                        Größe des Texts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 90, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'logo'), Attachment, scope=Configuration, documentation='\n                        Firmenlogo.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 97, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'background'), Attachment, scope=Configuration, documentation='\n                        Hintergrundbild.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 104, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'dummy_picture'), Attachment, scope=Configuration, documentation='\n                        Platzhalterbild.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 111, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hide_cursor'), pyxb.binding.datatypes.boolean, scope=Configuration, documentation='\n                        Soll der Cursor ausgeblendet werden?\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 118, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rotation'), pyxb.binding.datatypes.unsignedShort, scope=Configuration, documentation='\n                        Rotation in Grad.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 125, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'email_form'), pyxb.binding.datatypes.boolean, scope=Configuration, documentation='\n                        Soll ein E-Mail Formular angezeigt werden?\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 132, 12)))

Configuration._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'volume'), pyxb.binding.datatypes.unsignedShort, scope=Configuration, documentation='\n                        Lautstärke.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 139, 12)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 27, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 97, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 104, 12))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 111, 12))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 20, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 27, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'font')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 34, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'portrait')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 41, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'touch')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 48, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'design')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 55, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'effects')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 62, 12))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'ticker_speed')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 69, 12))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'colors')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 76, 12))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'title_size')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 83, 12))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'text_size')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 90, 12))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'logo')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 97, 12))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'background')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 104, 12))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'dummy_picture')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 111, 12))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'hide_cursor')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 118, 12))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'rotation')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 125, 12))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'email_form')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 132, 12))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Configuration._UseForTag(pyxb.namespace.ExpandedName(None, 'volume')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 139, 12))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    transitions.append(fac.Transition(st_12, [
         ]))
    transitions.append(fac.Transition(st_13, [
         ]))
    transitions.append(fac.Transition(st_14, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_2, False) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
        fac.UpdateInstruction(cc_3, True) ]))
    transitions.append(fac.Transition(st_14, [
        fac.UpdateInstruction(cc_3, False) ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
         ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    st_17._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Configuration._Automaton = _BuildAutomaton_3()




Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'header'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Farbe der Kopfzeile.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 157, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'header_background'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Hintergrundfarbe der Kopfzeile.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 164, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'background_left'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Hintergrundfarbe links.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 171, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'background_right'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Hintergrundfarbe rechts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 178, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ticker'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Farbe des Tickers.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 185, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ticker_background'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Hintergrundfarbe des Tickers.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 192, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'clock'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Farbe der Uhr.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 199, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Farbe des Titels.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 206, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Textfarbe.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 213, 12)))

Colors._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text_background'), pyxb.binding.datatypes.positiveInteger, scope=Colors, documentation='\n                        Hintergrundfarbe des Texts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 220, 12)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'header')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 157, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'header_background')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 164, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'background_left')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 171, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'background_right')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 178, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'ticker')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 185, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'ticker_background')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 192, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'clock')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 199, 12))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 206, 12))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 213, 12))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Colors._UseForTag(pyxb.namespace.ExpandedName(None, 'text_background')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/configuration.xsd', 220, 12))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    st_9._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Colors._Automaton = _BuildAutomaton_4()




Menu._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), pyxb.binding.datatypes.string, scope=Menu, documentation='\n                        Name des Menüs.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 19, 12)))

Menu._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.string, scope=Menu, documentation='\n                        Beschreibung des Menüs.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 26, 12)))

Menu._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'item'), MenuItem, scope=Menu, documentation='\n                        Menüelemente.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 33, 12)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 26, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 33, 12))
    counters.add(cc_1)
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Menu._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 19, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Menu._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 26, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Menu._UseForTag(pyxb.namespace.ExpandedName(None, 'item')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Menu._Automaton = _BuildAutomaton_5()




MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), pyxb.binding.datatypes.string, scope=MenuItem, documentation='\n                        Name des Menüelements.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 51, 12)))

MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'icon'), pyxb.binding.datatypes.string, scope=MenuItem, documentation='\n                        Symbol des Menüelements.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 58, 12)))

MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text_color'), pyxb.binding.datatypes.positiveInteger, scope=MenuItem, documentation='\n                        Schriftfarbe des Menüelements.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 65, 12)))

MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'background_color'), pyxb.binding.datatypes.positiveInteger, scope=MenuItem, documentation='\n                        Hintergrundfarbe des Menüelements.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 72, 12)))

MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'index'), pyxb.binding.datatypes.positiveInteger, scope=MenuItem, documentation='\n                        Position des Menüelements.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 79, 12)))

MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'child'), MenuItem, scope=MenuItem, documentation='\n                        Menüelemente.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 86, 12)))

MenuItem._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'chart'), MenuItemChart, scope=MenuItem, documentation='\n                        Charts, welche diesem Menüelement zugeordnet sind.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 93, 12)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 58, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 86, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 93, 12))
    counters.add(cc_2)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 51, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'icon')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 58, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'text_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 65, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'background_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 72, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'index')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 79, 12))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'child')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 86, 12))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(MenuItem._UseForTag(pyxb.namespace.ExpandedName(None, 'chart')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 93, 12))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MenuItem._Automaton = _BuildAutomaton_6()




MenuItemChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'chart_id'), pyxb.binding.datatypes.positiveInteger, scope=MenuItemChart, documentation='\n                        ID des entsprechenden Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 111, 12)))

MenuItemChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'chart_type'), pyxb.binding.datatypes.string, scope=MenuItemChart, documentation='\n                        Der Typ des entsprechenden Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 118, 12)))

MenuItemChart._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'index'), pyxb.binding.datatypes.positiveInteger, scope=MenuItemChart, documentation='\n                        Position des Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 125, 12)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MenuItemChart._UseForTag(pyxb.namespace.ExpandedName(None, 'chart_id')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 111, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(MenuItemChart._UseForTag(pyxb.namespace.ExpandedName(None, 'chart_type')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 118, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(MenuItemChart._UseForTag(pyxb.namespace.ExpandedName(None, 'index')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/menu.xsd', 125, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
MenuItemChart._Automaton = _BuildAutomaton_7()




FacebookAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'facebook_id'), pyxb.binding.datatypes.string, scope=FacebookAccount, documentation='\n                        Facebook ID.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 19, 12)))

FacebookAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'recent_days'), pyxb.binding.datatypes.unsignedShort, scope=FacebookAccount, documentation='\n                        Anzahl der letzten Tage.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 26, 12)))

FacebookAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'max_posts'), pyxb.binding.datatypes.unsignedShort, scope=FacebookAccount, documentation='\n                        Maximiale Anzahl an Posts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 33, 12)))

FacebookAccount._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'name'), pyxb.binding.datatypes.string, scope=FacebookAccount, documentation='\n                        Name des Kontos.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 40, 12)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 26, 12))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FacebookAccount._UseForTag(pyxb.namespace.ExpandedName(None, 'facebook_id')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 19, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FacebookAccount._UseForTag(pyxb.namespace.ExpandedName(None, 'recent_days')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 26, 12))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(FacebookAccount._UseForTag(pyxb.namespace.ExpandedName(None, 'max_posts')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 33, 12))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(FacebookAccount._UseForTag(pyxb.namespace.ExpandedName(None, 'name')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 40, 12))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    transitions.append(fac.Transition(st_2, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
FacebookAccount._Automaton = _BuildAutomaton_8()




Presentation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'configuration'), Configuration, scope=Presentation, documentation='\n                        Konfigurationen.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 33, 12)))

Presentation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'menu'), Menu, scope=Presentation, documentation='\n                        Menüs.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 40, 12)))

Presentation._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'chart'), Chart, scope=Presentation, documentation='\n                        Charts.\n                    ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 47, 12)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 33, 12))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 40, 12))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 47, 12))
    counters.add(cc_2)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Presentation._UseForTag(pyxb.namespace.ExpandedName(None, 'configuration')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 33, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(Presentation._UseForTag(pyxb.namespace.ExpandedName(None, 'menu')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 40, 12))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_2, False))
    symbol = pyxb.binding.content.ElementUse(Presentation._UseForTag(pyxb.namespace.ExpandedName(None, 'chart')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/presentation.xsd', 47, 12))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
Presentation._Automaton = _BuildAutomaton_9()




Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), pyxb.binding.datatypes.string, scope=Cleaning, documentation='\n                                Überschrift.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 116, 20)))

Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mode'), pyxb.binding.datatypes.string, scope=Cleaning, documentation='\n                                Modus des Charts.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 123, 20)))

Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), pyxb.binding.datatypes.string, scope=Cleaning, documentation='\n                                Textinhalt.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 130, 20)))

Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_size'), pyxb.binding.datatypes.unsignedShort, scope=Cleaning, documentation='\n                                Schriftgröße.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 137, 20)))

Cleaning._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text_color'), pyxb.binding.datatypes.positiveInteger, scope=Cleaning, documentation='\n                                Textfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 144, 20)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 130, 20))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 116, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'mode')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 123, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 130, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'font_size')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 137, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Cleaning._UseForTag(pyxb.namespace.ExpandedName(None, 'text_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 144, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    transitions.append(fac.Transition(st_4, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    st_5._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Cleaning._Automaton = _BuildAutomaton_10()




Facebook._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_size'), pyxb.binding.datatypes.unsignedShort, scope=Facebook, documentation='\n                                Schriftgröße.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 166, 20)))

Facebook._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title_color'), pyxb.binding.datatypes.positiveInteger, scope=Facebook, documentation='\n                                Textfarbe des Titels.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 173, 20)))

Facebook._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ken_burns'), pyxb.binding.datatypes.boolean, scope=Facebook, documentation='\n                                Ken Burns Effekt.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 180, 20)))

Facebook._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'account'), FacebookAccount, scope=Facebook, documentation='\n                                Facebook Konten.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 187, 20)))

def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 187, 20))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Facebook._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Facebook._UseForTag(pyxb.namespace.ExpandedName(None, 'font_size')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 166, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Facebook._UseForTag(pyxb.namespace.ExpandedName(None, 'title_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 173, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Facebook._UseForTag(pyxb.namespace.ExpandedName(None, 'ken_burns')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 180, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Facebook._UseForTag(pyxb.namespace.ExpandedName(None, 'account')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 187, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Facebook._Automaton = _BuildAutomaton_11()




Form._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'mode'), pyxb.binding.datatypes.string, scope=Form, documentation='\n                                Typ (Modus) des Formulars.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 209, 20)))

def _BuildAutomaton_12 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_12
    del _BuildAutomaton_12
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Form._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Form._UseForTag(pyxb.namespace.ExpandedName(None, 'mode')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 209, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Form._Automaton = _BuildAutomaton_12()




def _BuildAutomaton_13 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_13
    del _BuildAutomaton_13
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GarbageCollection._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
GarbageCollection._Automaton = _BuildAutomaton_13()




def _BuildAutomaton_14 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_14
    del _BuildAutomaton_14
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(GuessPicture._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
GuessPicture._Automaton = _BuildAutomaton_14()




ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'style'), pyxb.binding.datatypes.string, scope=ImageText, documentation='\n                                Stil des Charts.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 255, 20)))

ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title'), pyxb.binding.datatypes.string, scope=ImageText, documentation='\n                                Titel des Charts.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 262, 20)))

ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_size'), pyxb.binding.datatypes.unsignedShort, scope=ImageText, documentation='\n                                Schriftgröße.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 269, 20)))

ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title_color'), pyxb.binding.datatypes.positiveInteger, scope=ImageText, documentation='\n                                Titelfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 276, 20)))

ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ken_burns'), pyxb.binding.datatypes.boolean, scope=ImageText, documentation='\n                                Ken Burns Effekt.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 283, 20)))

ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'image'), Attachment, scope=ImageText, documentation='\n                                Bilder.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 290, 20)))

ImageText._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text'), pyxb.binding.datatypes.string, scope=ImageText, documentation='\n                                Texte.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 297, 20)))

def _BuildAutomaton_15 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_15
    del _BuildAutomaton_15
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 290, 20))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 297, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'style')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 255, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'title')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 262, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'font_size')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 269, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'title_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 276, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'ken_burns')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 283, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'image')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 290, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(ImageText._UseForTag(pyxb.namespace.ExpandedName(None, 'text')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 297, 20))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    transitions.append(fac.Transition(st_7, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_7._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ImageText._Automaton = _BuildAutomaton_15()




News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_size_title'), pyxb.binding.datatypes.unsignedShort, scope=News, documentation='\n                                Schriftgröße des Titles.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 319, 20)))

News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'title_color'), pyxb.binding.datatypes.positiveInteger, scope=News, documentation='\n                                Titelfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 326, 20)))

News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_size_text'), pyxb.binding.datatypes.unsignedShort, scope=News, documentation='\n                                Schriftgröße des Texts.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 333, 20)))

News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'text_color'), pyxb.binding.datatypes.positiveInteger, scope=News, documentation='\n                                Textfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 340, 20)))

News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ken_burns'), pyxb.binding.datatypes.boolean, scope=News, documentation='\n                                Ken Burns Effekt.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 347, 20)))

News._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'news_token'), pyxb.binding.datatypes.string, scope=News, documentation='\n                                Token zur Abfrage von News.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 354, 20)))

def _BuildAutomaton_16 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_16
    del _BuildAutomaton_16
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 347, 20))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 354, 20))
    counters.add(cc_1)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'font_size_title')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 319, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'title_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 326, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'font_size_text')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 333, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'text_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 340, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'ken_burns')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 347, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_1, False))
    symbol = pyxb.binding.content.ElementUse(News._UseForTag(pyxb.namespace.ExpandedName(None, 'news_token')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 354, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    transitions.append(fac.Transition(st_6, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
        fac.UpdateInstruction(cc_1, True) ]))
    st_6._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
News._Automaton = _BuildAutomaton_16()




def _BuildAutomaton_17 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_17
    del _BuildAutomaton_17
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(PublicTransport._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
PublicTransport._Automaton = _BuildAutomaton_17()




Quotes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_color'), pyxb.binding.datatypes.positiveInteger, scope=Quotes, documentation='\n                                Schriftfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 388, 20)))

Quotes._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'background_color'), pyxb.binding.datatypes.positiveInteger, scope=Quotes, documentation='\n                                Hintergrundfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 395, 20)))

def _BuildAutomaton_18 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_18
    del _BuildAutomaton_18
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Quotes._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Quotes._UseForTag(pyxb.namespace.ExpandedName(None, 'font_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 388, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Quotes._UseForTag(pyxb.namespace.ExpandedName(None, 'background_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 395, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Quotes._Automaton = _BuildAutomaton_18()




RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'display_format'), pyxb.binding.datatypes.string, scope=RealEstates, documentation='\n                                Anzeigeformat.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 417, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'ken_burns'), pyxb.binding.datatypes.boolean, scope=RealEstates, documentation='\n                                Ken Burns Effekt.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 424, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'scaling'), pyxb.binding.datatypes.boolean, scope=RealEstates, documentation='\n                                Soll die Application skalieren?\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 431, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'slideshow'), pyxb.binding.datatypes.boolean, scope=RealEstates, documentation='\n                                Soll die Application eine Slideshow anzeigen?\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 438, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'qr_codes'), pyxb.binding.datatypes.boolean, scope=RealEstates, documentation='\n                                Sollen QR Codes angezeigt werden?\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 445, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'show_contact'), pyxb.binding.datatypes.boolean, scope=RealEstates, documentation='\n                                Sollen Kontaktpersonen angezeigt werden?\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 452, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'contact_picture'), pyxb.binding.datatypes.boolean, scope=RealEstates, documentation='\n                                Sollen Bilder von Kontaktpersonen angezeigt werden?\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 459, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_size'), pyxb.binding.datatypes.unsignedShort, scope=RealEstates, documentation='\n                                Schriftgröße.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 466, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_color'), pyxb.binding.datatypes.positiveInteger, scope=RealEstates, documentation='\n                                Schriftfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 473, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'amenities'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 481, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'construction'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 482, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'courtage'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 483, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'floor'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 484, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'area'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 485, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'free_from'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 486, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'coop_share'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 487, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'total_area'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 488, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'plot_area'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 489, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cold_rent'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 490, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'purchase_price'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 491, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'security_deposit'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 492, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'service_charge'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 493, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'object_id'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 494, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'description'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 495, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'warm_rent'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 496, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 497, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lift'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 499, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'bathtub'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 500, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'balcony'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 501, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'accessibility'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 502, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'assited_living'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 503, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'carport'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 504, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'floorboards'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 505, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'duplex'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 506, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'shower'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 507, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'builtin_kitchen'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 508, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'screed'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 509, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'tiles'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 510, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'outdoor_parking'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 511, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'garage'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 512, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'cable_sat_tv'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 513, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'fireplace'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 514, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'basement'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 515, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'plastic'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 516, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'furnished'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 517, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'parquet'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 518, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'car_park'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 519, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'wheelchair_accessible'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 520, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'sauna'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 521, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'stone'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 522, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'swimming_pool'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 523, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'carpet'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 524, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'underground_carpark'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 525, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'lavatory'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 526, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms_1'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 528, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms_2'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 529, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms_3'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 530, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms_4'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 531, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms_5'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 532, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rooms_5_or_more'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 533, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'finance_project'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 535, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'business_realty'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 536, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'short_term_accommocation'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 537, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'living_realty'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 538, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'office'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 540, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'retail'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 541, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'recreational'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 542, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hospitality_industry'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 543, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'plot'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 544, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'hall_warehouse_production'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 545, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'house'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 546, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'agriculture_forestry'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 547, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'miscellaneous'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 548, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'flat'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 549, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'room'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 550, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'income_property'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 551, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'emphyteusis'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 553, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'leasing'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 554, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'rent'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 555, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'sale'), pyxb.binding.datatypes.boolean, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 556, 20)))

RealEstates._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'filter'), Filter, scope=RealEstates, location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 558, 20)))

def _BuildAutomaton_19 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_19
    del _BuildAutomaton_19
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 558, 20))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'display_format')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 417, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'ken_burns')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 424, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'scaling')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 431, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'slideshow')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 438, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'qr_codes')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 445, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'show_contact')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 452, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'contact_picture')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 459, 20))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'font_size')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 466, 20))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'font_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 473, 20))
    st_9 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_9)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'amenities')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 481, 20))
    st_10 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_10)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'construction')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 482, 20))
    st_11 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_11)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'courtage')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 483, 20))
    st_12 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_12)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'floor')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 484, 20))
    st_13 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_13)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'area')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 485, 20))
    st_14 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_14)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'free_from')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 486, 20))
    st_15 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_15)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'coop_share')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 487, 20))
    st_16 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_16)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'total_area')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 488, 20))
    st_17 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_17)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'plot_area')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 489, 20))
    st_18 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_18)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'cold_rent')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 490, 20))
    st_19 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_19)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'purchase_price')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 491, 20))
    st_20 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_20)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'security_deposit')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 492, 20))
    st_21 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_21)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'service_charge')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 493, 20))
    st_22 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_22)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'object_id')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 494, 20))
    st_23 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_23)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'description')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 495, 20))
    st_24 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_24)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'warm_rent')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 496, 20))
    st_25 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_25)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 497, 20))
    st_26 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_26)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'lift')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 499, 20))
    st_27 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_27)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'bathtub')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 500, 20))
    st_28 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_28)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'balcony')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 501, 20))
    st_29 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_29)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'accessibility')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 502, 20))
    st_30 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_30)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'assited_living')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 503, 20))
    st_31 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_31)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'carport')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 504, 20))
    st_32 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_32)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'floorboards')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 505, 20))
    st_33 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_33)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'duplex')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 506, 20))
    st_34 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_34)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'shower')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 507, 20))
    st_35 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_35)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'builtin_kitchen')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 508, 20))
    st_36 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_36)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'screed')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 509, 20))
    st_37 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_37)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'tiles')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 510, 20))
    st_38 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_38)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'outdoor_parking')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 511, 20))
    st_39 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_39)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'garage')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 512, 20))
    st_40 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_40)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'cable_sat_tv')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 513, 20))
    st_41 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_41)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'fireplace')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 514, 20))
    st_42 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_42)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'basement')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 515, 20))
    st_43 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_43)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'plastic')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 516, 20))
    st_44 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_44)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'furnished')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 517, 20))
    st_45 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_45)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'parquet')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 518, 20))
    st_46 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_46)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'car_park')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 519, 20))
    st_47 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_47)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'wheelchair_accessible')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 520, 20))
    st_48 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_48)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'sauna')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 521, 20))
    st_49 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_49)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'stone')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 522, 20))
    st_50 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_50)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'swimming_pool')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 523, 20))
    st_51 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_51)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'carpet')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 524, 20))
    st_52 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_52)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'underground_carpark')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 525, 20))
    st_53 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_53)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'lavatory')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 526, 20))
    st_54 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_54)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms_1')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 528, 20))
    st_55 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_55)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms_2')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 529, 20))
    st_56 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_56)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms_3')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 530, 20))
    st_57 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_57)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms_4')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 531, 20))
    st_58 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_58)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms_5')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 532, 20))
    st_59 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_59)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rooms_5_or_more')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 533, 20))
    st_60 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_60)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'finance_project')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 535, 20))
    st_61 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_61)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'business_realty')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 536, 20))
    st_62 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_62)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'short_term_accommocation')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 537, 20))
    st_63 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_63)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'living_realty')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 538, 20))
    st_64 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_64)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'office')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 540, 20))
    st_65 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_65)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'retail')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 541, 20))
    st_66 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_66)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'recreational')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 542, 20))
    st_67 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_67)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'hospitality_industry')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 543, 20))
    st_68 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_68)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'plot')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 544, 20))
    st_69 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_69)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'hall_warehouse_production')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 545, 20))
    st_70 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_70)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'house')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 546, 20))
    st_71 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_71)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'agriculture_forestry')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 547, 20))
    st_72 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_72)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'miscellaneous')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 548, 20))
    st_73 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_73)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'flat')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 549, 20))
    st_74 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_74)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'room')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 550, 20))
    st_75 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_75)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'income_property')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 551, 20))
    st_76 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_76)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'emphyteusis')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 553, 20))
    st_77 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_77)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'leasing')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 554, 20))
    st_78 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_78)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'rent')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 555, 20))
    st_79 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_79)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'sale')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 556, 20))
    st_80 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_80)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(RealEstates._UseForTag(pyxb.namespace.ExpandedName(None, 'filter')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 558, 20))
    st_81 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_81)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_9, [
         ]))
    st_8._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_10, [
         ]))
    st_9._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_11, [
         ]))
    st_10._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_12, [
         ]))
    st_11._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_13, [
         ]))
    st_12._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_14, [
         ]))
    st_13._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_15, [
         ]))
    st_14._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_16, [
         ]))
    st_15._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_17, [
         ]))
    st_16._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_18, [
         ]))
    st_17._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_19, [
         ]))
    st_18._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_20, [
         ]))
    st_19._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_21, [
         ]))
    st_20._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_22, [
         ]))
    st_21._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_23, [
         ]))
    st_22._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_24, [
         ]))
    st_23._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_25, [
         ]))
    st_24._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_26, [
         ]))
    st_25._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_27, [
         ]))
    st_26._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_28, [
         ]))
    st_27._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_29, [
         ]))
    st_28._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_30, [
         ]))
    st_29._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_31, [
         ]))
    st_30._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_32, [
         ]))
    st_31._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_33, [
         ]))
    st_32._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_34, [
         ]))
    st_33._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_35, [
         ]))
    st_34._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_36, [
         ]))
    st_35._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_37, [
         ]))
    st_36._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_38, [
         ]))
    st_37._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_39, [
         ]))
    st_38._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_40, [
         ]))
    st_39._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_41, [
         ]))
    st_40._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_42, [
         ]))
    st_41._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_43, [
         ]))
    st_42._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_44, [
         ]))
    st_43._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_45, [
         ]))
    st_44._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_46, [
         ]))
    st_45._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_47, [
         ]))
    st_46._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_48, [
         ]))
    st_47._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_49, [
         ]))
    st_48._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_50, [
         ]))
    st_49._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_51, [
         ]))
    st_50._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_52, [
         ]))
    st_51._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_53, [
         ]))
    st_52._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_54, [
         ]))
    st_53._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_55, [
         ]))
    st_54._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_56, [
         ]))
    st_55._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_57, [
         ]))
    st_56._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_58, [
         ]))
    st_57._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_59, [
         ]))
    st_58._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_60, [
         ]))
    st_59._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_61, [
         ]))
    st_60._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_62, [
         ]))
    st_61._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_63, [
         ]))
    st_62._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_64, [
         ]))
    st_63._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_65, [
         ]))
    st_64._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_66, [
         ]))
    st_65._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_67, [
         ]))
    st_66._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_68, [
         ]))
    st_67._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_69, [
         ]))
    st_68._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_70, [
         ]))
    st_69._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_71, [
         ]))
    st_70._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_72, [
         ]))
    st_71._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_73, [
         ]))
    st_72._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_74, [
         ]))
    st_73._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_75, [
         ]))
    st_74._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_76, [
         ]))
    st_75._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_77, [
         ]))
    st_76._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_78, [
         ]))
    st_77._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_79, [
         ]))
    st_78._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_80, [
         ]))
    st_79._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_81, [
         ]))
    st_80._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_81, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_81._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
RealEstates._Automaton = _BuildAutomaton_19()




Video._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'video'), Attachment, scope=Video, documentation='\n                                Das entsprechende Video.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 574, 20)))

def _BuildAutomaton_20 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_20
    del _BuildAutomaton_20
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Video._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Video._UseForTag(pyxb.namespace.ExpandedName(None, 'video')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 574, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Video._Automaton = _BuildAutomaton_20()




Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'location'), pyxb.binding.datatypes.string, scope=Weather, documentation='\n                                Ort des Wetters.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 596, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'font_color'), pyxb.binding.datatypes.positiveInteger, scope=Weather, documentation='\n                                Schriftfarbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 603, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'icon_color'), pyxb.binding.datatypes.positiveInteger, scope=Weather, documentation='\n                                Icon Farbe.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 610, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'box_color_top'), pyxb.binding.datatypes.positiveInteger, scope=Weather, documentation='\n                                Obere Farbe der Box.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 617, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'box_color_middle'), pyxb.binding.datatypes.positiveInteger, scope=Weather, documentation='\n                                Mittlere Farbe der Box.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 624, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'box_color_bottom'), pyxb.binding.datatypes.positiveInteger, scope=Weather, documentation='\n                                Untere Farbe der Box.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 631, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'transparency'), pyxb.binding.datatypes.positiveInteger, scope=Weather, documentation='\n                                Transparenz.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 638, 20)))

Weather._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'image'), Attachment, scope=Weather, documentation='\n                                Bilder.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 645, 20)))

def _BuildAutomaton_21 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_21
    del _BuildAutomaton_21
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 645, 20))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'base')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 82, 12))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'location')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 596, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'font_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 603, 20))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'icon_color')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 610, 20))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'box_color_top')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 617, 20))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'box_color_middle')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 624, 20))
    st_5 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_5)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'box_color_bottom')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 631, 20))
    st_6 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_6)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'transparency')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 638, 20))
    st_7 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_7)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(Weather._UseForTag(pyxb.namespace.ExpandedName(None, 'image')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/charts.xsd', 645, 20))
    st_8 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_8)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_3, [
         ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_5, [
         ]))
    st_4._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_6, [
         ]))
    st_5._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_7, [
         ]))
    st_6._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
         ]))
    st_7._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_8, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_8._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
Weather._Automaton = _BuildAutomaton_21()




IdFilter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'value'), pyxb.binding.datatypes.string, scope=IdFilter, documentation='\n                                Wert der ID.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 69, 20)))

IdFilter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'type'), pyxb.binding.datatypes.string, scope=IdFilter, documentation='\n                                Typ der ID.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 76, 20)))

def _BuildAutomaton_22 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_22
    del _BuildAutomaton_22
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(IdFilter._UseForTag(pyxb.namespace.ExpandedName(None, 'value')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 69, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(IdFilter._UseForTag(pyxb.namespace.ExpandedName(None, 'type')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 76, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
IdFilter._Automaton = _BuildAutomaton_22()




ZipCodeFilter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'zip_code'), pyxb.binding.datatypes.string, scope=ZipCodeFilter, documentation='\n                                Postleitzahl.\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 98, 20)))

ZipCodeFilter._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(None, 'blacklist'), pyxb.binding.datatypes.boolean, scope=ZipCodeFilter, documentation='\n                                Handelt es sich um eine Blacklist (true) oder Whitelist(false)?\n                            ', location=pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 105, 20)))

def _BuildAutomaton_23 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_23
    del _BuildAutomaton_23
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(ZipCodeFilter._UseForTag(pyxb.namespace.ExpandedName(None, 'zip_code')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 98, 20))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(ZipCodeFilter._UseForTag(pyxb.namespace.ExpandedName(None, 'blacklist')), pyxb.utils.utility.Location('/home/neumann/Projects/dscms4/files/xsd/misc.xsd', 105, 20))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
ZipCodeFilter._Automaton = _BuildAutomaton_23()

