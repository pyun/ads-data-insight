"""Model Context Protocol server for Trino using stdio transport.

This module provides a Model Context Protocol (MCP) server that exposes Trino
functionality through resources and tools, with special support for Iceberg tables.
It uses stdio for communication instead of SSE.
"""

from pydantic import Field

from strands import tool

from config import load_config, TrinoConfig
from trino_client import TrinoClient

class TrinoTools:
    def __init__(self, config: dict = None):
        if config:
            self.config = TrinoConfig(
                host=config.get('host'),
                port=int(config.get('port', 8889)),
                user=config.get('user'),
                catalog=config.get('catalog'),
                schema=config.get('schema'),
                http_scheme=config.get('http_scheme', 'http'),
                auth=config.get('auth'),
                source=config.get('source', 'mcp-trino-python')
            )
        else:
            self.config = load_config()
        self.client = TrinoClient(self.config)

    # Tools
    @tool(description="List all available catalogs")
    def show_catalogs(self) -> str:
        """List all available catalogs."""
        return self.client.list_catalogs()


    @tool(description="List all schemas in a catalog")
    def show_schemas(self, catalog: str = Field(description="The name of the catalog")) -> str:
        """List all schemas in a catalog.

        Args:
            catalog: The name of the catalog

        Returns:
            str: List of schemas in the specified catalog
        """
        return self.client.list_schemas(catalog)


    @tool(description="List all tables in a schema")
    def show_tables(
        self,
        catalog: str = Field(description="The name of the catalog"),
        schema_name: str = Field(description="The name of the schema"),
    ) -> str:
        """List all tables in a schema.

        Args:
            catalog: The name of the catalog
            schema_name: The name of the schema

        Returns:
            str: List of tables in the specified schema
        """
        return self.client.list_tables(catalog, schema_name)


    @tool(description="Describe a table")
    def describe_table(
        self,
        catalog: str = Field(description="The catalog name"),
        schema_name: str = Field(description="The schema name"),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Describe a table.

        Args:
            catalog (str): The catalog name
            schema_name (str): The schema name
            table (str): The name of the table

        Returns:
            str: Table description in JSON format
        """
        return self.client.describe_table(catalog, schema_name, table)


    @tool(description="Show the CREATE TABLE statement for a specific table")
    def show_create_table(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show the CREATE TABLE statement for a table.

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: The CREATE TABLE statement
        """
        return self.client.show_create_table(catalog, schema_name, table)


    @tool(description="Show the CREATE VIEW statement for a specific view")
    def show_create_view(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        view: str = Field(description="The name of the view"),
    ) -> str:
        """Show the CREATE VIEW statement for a view.

        Args:
            catalog: catalog name
            schema_name:  schema name
            view: The name of the view

        Returns:
            str: The CREATE VIEW statement
        """
        return self.client.show_create_view(catalog, schema_name, view)


    @tool(description="Execute a SQL query and return results in a readable format")
    def execute_query(self, query: str = Field(description="The SQL query to execute")) -> str:
        """Execute a SQL query and return formatted results.

        Args:
            query: The SQL query to execute

        Returns:
            str: Query results formatted as a JSON string
        """
        return self.client.execute_query(query)


    @tool(description="Optimize an Iceberg table's data files")
    def optimize(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table to optimize"),
    ) -> str:
        """Optimize an Iceberg table by compacting small files.

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table to optimize

        Returns:
            str: Confirmation message
        """
        return self.client.optimize(catalog, schema_name, table)


    @tool(description="Optimize manifest files for an Iceberg table")
    def optimize_manifests(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Optimize manifest files for an Iceberg table.

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: Confirmation message
        """
        return self.client.optimize_manifests(catalog, schema_name, table)


    @tool(description="Remove old snapshots from an Iceberg table")
    def expire_snapshots(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        retention_threshold: str = Field(
            description="Age threshold for snapshot removal (e.g., '7d', '30d')", default="7d"
        ),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Remove old snapshots from an Iceberg table.

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table
            retention_threshold: Age threshold for snapshot removal (e.g., "7d", "30d")

        Returns:
            str: Confirmation message
        """
        return self.client.expire_snapshots(catalog, schema_name, table, retention_threshold)


    @tool(description="Show statistics for a table")
    def show_stats(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show statistics for a table.

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: Table statistics in JSON format
        """
        return self.client.show_stats(catalog, schema_name, table)


    @tool(name="show_query_history", description="Get the history of executed queries")
    def show_query_history(
        self,
        limit: int = Field(description="maximum number of history entries to return", default=None),
    ) -> str:
        """Get the history of executed queries.

        Args:
            limit: maximum number of history entries to return.
                If None, returns all entries.

        Returns:
            str: JSON-formatted string containing query history.
        """
        return self.client.get_query_history(limit)


    @tool(description="Show a hierarchical tree view of catalogs, schemas, and tables")
    def show_catalog_tree(self) -> str:
        """Get a hierarchical tree view showing the full structure of catalogs, schemas, and tables.

        Returns:
            str: A formatted string showing the catalog > schema > table hierarchy with visual indicators
        """
        return self.client.show_catalog_tree()


    @tool(description="Show Iceberg table properties")
    def show_table_properties(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table properties.

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted table properties
        """
        return self.client.show_table_properties(catalog, schema_name, table)


    @tool(description="Show Iceberg table history/changelog")
    def show_table_history(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table history/changelog.

        The history contains:
        - made_current_at: When snapshot became active
        - snapshot_id: Identifier of the snapshot
        - parent_id: Identifier of the parent snapshot
        - is_current_ancestor: Whether snapshot is an ancestor of current

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted table history
        """
        return self.client.show_table_history(catalog, schema_name, table)


    @tool(description="Show metadata for the table")
    def show_metadata_log_entries(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table metadata log entries.

        The metadata log contains:
        - timestamp: When metadata was created
        - file: Location of the metadata file
        - latest_snapshot_id: ID of latest snapshot when metadata was updated
        - latest_schema_id: ID of latest schema when metadata was updated
        - latest_sequence_number: Data sequence number of metadata file

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted metadata log entries
        """
        return self.client.show_metadata_log_entries(catalog, schema_name, table)


    @tool(description="Show Iceberg table snapshots")
    def show_snapshots(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table snapshots.

        The snapshots table contains:
        - committed_at: When snapshot became active
        - snapshot_id: Identifier for the snapshot
        - parent_id: Identifier for the parent snapshot
        - operation: Type of operation (append/replace/overwrite/delete)
        - manifest_list: List of Avro manifest files
        - summary: Summary of changes from previous snapshot

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted table snapshots
        """
        return self.client.show_snapshots(catalog, schema_name, table)


    @tool(description="Show Iceberg table manifests")
    def show_manifests(
        self,
        catalog: str = Field(description="catalog name"),
        schema_name: str = Field(description="schema name"),
        table: str = Field(description="The name of the table"),
        all_snapshots: bool = False,
    ) -> str:
        """Show Iceberg table manifests for current or all snapshots.

        The manifests table contains:
        - path: Manifest file location
        - length: Manifest file length
        - partition_spec_id: ID of partition spec used
        - added_snapshot_id: ID of snapshot when manifest was added
        - added_data_files_count: Number of data files with status ADDED
        - added_rows_count: Total rows in ADDED files
        - existing_data_files_count: Number of EXISTING files
        - existing_rows_count: Total rows in EXISTING files
        - deleted_data_files_count: Number of DELETED files
        - deleted_rows_count: Total rows in DELETED files
        - partition_summaries: Partition range metadata

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table
            all_snapshots: If True, show manifests from all snapshots

        Returns:
            str: JSON-formatted table manifests
        """
        return self.client.show_manifests(catalog, schema_name, table, all_snapshots)


    @tool(description="Show Iceberg table partitions")
    def show_partitions(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table partitions.

        The partitions table contains:
        - partition: Mapping of partition column names to values
        - record_count: Number of records in partition
        - file_count: Number of files in partition
        - total_size: Total size of files in partition
        - data: Partition range metadata with min/max values and null/nan counts

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted table partitions
        """
        return self.client.show_partitions(catalog, schema_name, table)


    @tool(description="Show Iceberg table data files")
    def show_files(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table data files in current snapshot.

        The files table contains:
        - content: Type of content (0=DATA, 1=POSITION_DELETES, 2=EQUALITY_DELETES)
        - file_path: Data file location
        - file_format: Format of the data file
        - record_count: Number of records in file
        - file_size_in_bytes: File size
        - column_sizes: Column ID to size mapping
        - value_counts: Column ID to value count mapping
        - null_value_counts: Column ID to null count mapping
        - nan_value_counts: Column ID to NaN count mapping
        - lower_bounds: Column ID to lower bound mapping
        - upper_bounds: Column ID to upper bound mapping
        - key_metadata: Encryption key metadata
        - split_offsets: Recommended split locations
        - equality_ids: Field IDs for equality deletes

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted table files info
        """
        return self.client.show_files(catalog, schema_name, table)


    @tool(description="Show Iceberg table manifest entries")
    def show_entries(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
        all_snapshots: bool = False,
    ) -> str:
        """Show Iceberg table manifest entries for current or all snapshots.

        The entries table contains:
        - status: Status of entry (0=EXISTING, 1=ADDED, 2=DELETED)
        - snapshot_id: ID of the snapshot
        - sequence_number: Data sequence number
        - file_sequence_number: File sequence number
        - data_file: File metadata including path, format, size etc
        - readable_metrics: Human-readable file metrics

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table
            all_snapshots: If True, show entries from all snapshots

        Returns:
            str: JSON-formatted manifest entries
        """
        return self.client.show_entries(catalog, schema_name, table, all_snapshots)


    @tool(description="Show Iceberg table references (branches and tags)")
    def show_refs(
        self,
        catalog: str = Field(description="catalog name "),
        schema_name: str = Field(description="schema name "),
        table: str = Field(description="The name of the table"),
    ) -> str:
        """Show Iceberg table references (branches and tags).

        The refs table contains:
        - name: Name of the reference
        - type: Type of reference (BRANCH or TAG)
        - snapshot_id: ID of referenced snapshot
        - max_reference_age_in_ms: Max age before reference expiry
        - min_snapshots_to_keep: Min snapshots to keep (branches only)
        - max_snapshot_age_in_ms: Max snapshot age in branch

        Args:
            catalog: catalog name
            schema_name: schema name
            table: The name of the table

        Returns:
            str: JSON-formatted table references
        """
        return self.client.show_refs(catalog, schema_name, table)
    
    def list_tools(self):
        """List all available tools."""
        return [getattr(self, method) for method in dir(self) if callable(getattr(self, method)) and not method.startswith('_')]