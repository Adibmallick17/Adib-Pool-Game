#ifndef PHYLIB_H
#define PHYLIB_H

// Constants
#define PHYLIB_BALL_RADIUS (28.5) // mm
#define PHYLIB_BALL_DIAMETER (2*PHYLIB_BALL_RADIUS)
#define PHYLIB_HOLE_RADIUS (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH (2700.0) // mm
#define PHYLIB_TABLE_WIDTH (PHYLIB_TABLE_LENGTH/2.0) // mm
#define PHYLIB_SIM_RATE (0.0001) // s
#define PHYLIB_VEL_EPSILON (0.01) // mm/s
#define PHYLIB_DRAG (150.0) // mm/s^2
#define PHYLIB_MAX_TIME (600) // s
#define PHYLIB_MAX_OBJECTS (26) 

// Coordinate structure
typedef struct {
    double x;
    double y;
} phylib_coord;

// Object types
typedef enum {
    PHYLIB_STILL_BALL,
    PHYLIB_ROLLING_BALL,
    PHYLIB_HOLE,
    PHYLIB_HCUSHION,
    PHYLIB_VCUSHION
} phylib_obj; 

// Object structure
typedef struct {
    phylib_obj type;
    union {
        struct {
            unsigned char number;
            phylib_coord pos;
        } still_ball;
        struct {
            unsigned char number;
            phylib_coord pos;
            phylib_coord vel;
            phylib_coord acc;
        } rolling_ball;
        struct {
            phylib_coord pos;
        } hole;
        struct {
            double y;
        } hcushion;
        struct {
            double x;
        } vcushion;
    } obj;
} phylib_object;

// Table structure
typedef struct {
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

// Function prototypes
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos);
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc);
phylib_object *phylib_new_hole(phylib_coord *pos);
phylib_object *phylib_new_hcushion(double y);
phylib_object *phylib_new_vcushion(double x);
phylib_table *phylib_new_table(void);
void phylib_copy_object(phylib_object **dest, phylib_object **src);
phylib_table *phylib_copy_table(phylib_table *table);
void phylib_add_object(phylib_table *table, phylib_object *object);
void phylib_free_table(phylib_table *table);
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2);
double phylib_length(phylib_coord c);
double phylib_dot_product(phylib_coord a, phylib_coord b);
double phylib_distance(phylib_object *obj1, phylib_object *obj2);
void phylib_roll(phylib_object *new, phylib_object *old, double time);
unsigned char phylib_stopped(phylib_object *object);
void phylib_bounce(phylib_object **a, phylib_object **b);
unsigned char phylib_rolling(phylib_table *t);
phylib_table *phylib_segment(phylib_table *table);
void phylib_free_object(phylib_object *object);
phylib_coord phylib_normalize(phylib_coord c);
phylib_coord phylib_reflect(phylib_coord v, phylib_coord n);
phylib_coord phylib_compute_next_pos(phylib_object *obj);
void phylib_update_table(phylib_table *table, double elapsed_time);
char *phylib_object_string(phylib_object *object);

#endif  // PHYLIB_H

