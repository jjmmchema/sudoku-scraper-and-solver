

# tiles_to_update = np.concatenate((editable_same_row_tile, editable_same_col_tile))

# if tiles_to_update.size == 0:
#     idx_to_remove = np.where(possible_values == choice)
#     possible_values = np.delete(possible_values, idx_to_remove)
#     continue

# self.update_tile(tile, choice, vals, "red")

# while tiles_to_update.size > 0:
#     t = tiles_to_update[0]
#     self.find_and_update_tile_value(t, vals)
#     np.delete(tiles_to_update, 0)

# break


# if editable_same_row_tile.size == 0 and editable_same_col_tile.size == 0:
#     self.update_tile(tile, choice, vals, "red")
#     break