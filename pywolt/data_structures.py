from typing import List, Optional, Tuple, Dict, Any
from pydantic_extra_types.currency_code import ISO4217
from pydantic_extra_types.country import CountryAlpha3
from pydantic import BaseModel, HttpUrl


class SortingSortables(BaseModel):
    """
    Sortable options for sorting venues.
    """

    id: str
    value: int


class FilteringFilters(BaseModel):
    """
    Filtering options for filtering venues.
    """

    id: str
    values: List[str]


class VenueRating(BaseModel):
    """
    Rating of a venue.
    """

    rating: int
    score: float


class Image(BaseModel):
    """
    Image associated with a venue.
    """

    blurhash: Optional[str]
    url: HttpUrl


class Link(BaseModel):
    """
    Link associated with a venue.
    """

    selected_delivery_method: str
    target: str
    target_sort: str
    target_title: str
    title: str
    type: str
    venue_mainimage_blurhash: str


class OverlayV2(BaseModel):
    """
    Represents an overlay for a venue.
    """

    icon: Optional[str] | None = None
    primary_text: str
    secondary_text: Optional[str] | None = None
    telemetry_status: str
    variant: str


class Venue(BaseModel):
    """
    Represents a venue (e.g., restaurant, grocery shop) that can be ordered from.
    """

    address: str
    badges: List[dict]
    badges_v2: List[str]
    categories: List[str]
    city: str
    country: CountryAlpha3
    currency: ISO4217
    delivers: bool
    delivery_price: Optional[str | dict] | None = None
    delivery_price_highlight: bool
    delivery_price_int: Optional[int] | None = None
    estimate: int
    estimate_range: str
    franchise: str
    icon: Optional[str] | None = None
    id: str
    location: Tuple[float, float]
    name: str
    online: bool
    price_range: int
    product_line: str
    promotions: List[Dict[str, str]]
    rating: Optional[VenueRating] | None = None
    short_description: Optional[str] | None = None
    show_wolt_plus: bool
    slug: str
    tags: List[str]


class VenueData(BaseModel):
    """
    Represents data associated with a venue.
    """

    filtering: Dict[str, List[FilteringFilters]]
    image: Image
    link: Link
    sorting: Dict
    telemetry_venue_badges: List[str]
    template: str
    title: str
    track_id: str
    venue: Venue
    overlay: Optional[str] | None = None
    overlay_v2: Optional[OverlayV2] | None = None

    def __repr__(self):
        open_status = "Open" if self.venue.online else "Closed"
        price_range_desc = {
            1: "💲",
            2: "💲💲",
            3: "💲💲💲",
            4: "💲💲💲💲",
            5: "💲💲💲💲💲",
        }.get(self.venue.price_range, "Unknown")

        tags_str = (
            ", ".join(self.venue.tags) if self.venue.tags else "No tags available"
        )

        delivery_estimate = (
            f"{self.venue.estimate} mins" if self.venue.estimate else "Not available"
        )

        additional_fields = [
            f"Delivery Price: {self.venue.delivery_price}",
            (
                f"Score: {self.venue.rating.score}"
                if self.venue.rating
                else "No rating available"
            ),
        ]

        return (
            f"Address: {self.venue.address}\n"
            f"Price Range: {price_range_desc}\n"
            f"Status: {open_status}\n"
            f"Tags: {tags_str}\n"
            f"Delivery Estimate: {delivery_estimate}\n" + "\n".join(additional_fields)
        )


class MenuItemOption(BaseModel):
    """
    Represents an option for a menu item, which may have multiple choices.
    """

    id: str
    name: str
    maximum_single_selections: int
    maximum_total_selections: int
    minimum_total_selections: int
    parent: str
    required_option_selections: list

    def __repr__(self):
        return (
            f"Name: {self.name}\n"
            f"Price: {self.baseprice/100}₪\n"
            f"Availability: {'Available' if self.enabled else 'Not available'}\n"
        )


class MenuItem(BaseModel):
    """
    Represents a single item from a venue's menu.
    """

    advertising_badge: Optional[str]
    advertising_metadata: Optional[Dict[str, Any]]
    alcohol_percentage: float
    allowed_delivery_methods: List[str]
    barcode_gtin: Optional[str]
    baseprice: int
    brand_id: Optional[str]
    caffeine_content: Optional[str]
    category: str
    checksum: str
    deposit: Optional[float]
    deposit_type: Optional[str]
    description: str
    dietary_preferences: List[str]
    disabled_info: Optional[Dict[str, Any]]
    enabled: bool
    exclude_from_discounts: bool
    exclude_from_discounts_min_basket: bool
    fulfillment_lead_time: Optional[int]
    has_extra_info: bool
    id: str
    images: List[Image]
    is_cutlery: bool
    lowest_historical_price: Optional[float]
    mandatory_warnings: List[str]
    max_quantity_per_purchase: Optional[int]
    min_quantity_per_purchase: Optional[int]
    name: str
    no_contact_delivery_allowed: bool
    options: List[MenuItemOption]
    original_price: Optional[float]
    quantity_left: Optional[int]
    quantity_left_visible: bool
    restrictions: Optional[List[Dict]]
    return_policy: Optional[str]
    sell_by_weight_config: Optional[Dict[str, Any]]
    tags: List[dict]
    times: List[Dict[str, Any]]
    type: str
    unformatted_unit_price: Optional[Dict]
    unit_info: Optional[str]
    unit_price: Optional[str]
    validity: Optional[dict]
    vat_percentage: float
    wolt_plus_only: bool

    def __repr__(self):
        return (
            f"Description: {self.description}\n"
            f"Price: {self.baseprice/100}₪\n"
            f"Availability: {'Available' if self.enabled else 'Not available'}\n"
        )


class Language(BaseModel):
    autotranslated: bool
    language: str
    name: str


class AssortmentSubcategory(BaseModel):
    id: str
    description: str
    images: List[Image]
    name: str
    slug: str
    subcategories: List['AssortmentSubcategory']
    item_ids: List[str]


class Category(BaseModel):
    id: str
    description: str
    images: List[Image]
    name: str
    slug: str


class AssortmentCategory(Category):
    subcategories: List[AssortmentSubcategory]
    item_ids: List[str]


class ComplianceInfo(BaseModel):
    badges: List[str]
    disclaimers: Optional[str]
    how_search_works: Optional[str]
    lowest_price_calculation_interval_in_days: int
    should_display_original_price_for_unit_price: bool
    should_display_price_by_subtracting_deposit: bool


class AssortmentResponse(BaseModel):
    assortment_id: str
    loading_strategy: str
    primary_language: str
    selected_language: str
    available_languages: List[Language]
    compliance_info: ComplianceInfo
    categories: List[AssortmentCategory]
    items: List[str]
    options: List[str]
    variant_groups: List[str]


class AvailableTime(BaseModel):
    days: List[int]
    start_time: int
    end_time: int


class Promotion(BaseModel):
    basket: bool
    venue: bool


class UnitPrice(BaseModel):
    base: int
    original_price: Optional[int]
    price: int
    unit: str


class RestrictionInfo(BaseModel):
    type: str
    age_limit: Optional[int]


class Item(BaseModel):
    id: str
    advertising_info: Optional[str]
    alcohol_permille: int
    allowed_delivery_methods: List[str]
    available_times: List[AvailableTime]
    barcode_gtin: Optional[str]
    caffeine_info: Optional[str]
    can_be_promoted: Promotion
    checksum: str
    description: str
    deposit: Optional[str]
    dietary_preferences: List[str]
    disabled_info: Optional[Dict[str, Any]]
    fulfillment_lead_time: Optional[int]
    has_extra_info: bool
    images: List[Image]
    is_cutlery: bool
    is_no_contact_delivery_allowed: bool
    is_wolt_plus_only: bool
    lowest_price: Optional[int]
    max_quantity_per_purchase: Optional[int]
    min_quantity_per_purchase: Optional[int]
    name: str
    options: List[Dict[str, Any]]
    original_price: Optional[int]
    price: int
    purchasable_balance: Optional[int]
    restrictions: List[RestrictionInfo]
    return_policy: Optional[str]
    sell_by_weight_config: Optional[Dict[str, Any]]
    should_display_purchasable_balance: bool
    tags: List[Optional[Dict[str, Any]]]
    unit_info: Optional[str]
    unit_price: Optional[UnitPrice]
    variant: Optional[str]


class CategoryMetadata(BaseModel):
    next_page_token: Optional[str]
    page: int


class CategoryItemsResponse(BaseModel):
    category: Category
    items: List[Item]
    options: List[Dict[str, Any]]
    variant_groups: List[str]
    metadata: CategoryMetadata
