#include "phylib.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

// Create a new still ball object
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));
    if (obj == NULL)
    {
        return NULL;
    }

    obj->type = PHYLIB_STILL_BALL;
    obj->obj.still_ball.number = number;
    obj->obj.still_ball.pos = *pos;

    return obj;
}

// Create a new rolling ball object
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc)
{
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));
    if (obj == NULL)
    {
        return NULL;
    }

    obj->type = PHYLIB_ROLLING_BALL;
    obj->obj.rolling_ball.number = number;
    obj->obj.rolling_ball.vel = *vel;
    obj->obj.rolling_ball.acc = *acc;
    obj->obj.rolling_ball.pos = *pos;
    return obj;
}

// Create a new hole object
phylib_object *phylib_new_hole(phylib_coord *pos)
{
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));
    if (obj == NULL)
    {
        return NULL;
    }

    obj->type = PHYLIB_HOLE;
    obj->obj.hole.pos = *pos;

    return obj;
}

// Create a new horizontal cushion object
phylib_object *phylib_new_hcushion(double y)
{
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));
    if (obj == NULL)
    {
        return NULL;
    }

    obj->type = PHYLIB_HCUSHION;
    obj->obj.hcushion.y = y;

    return obj;
}

// Create a new vertical cushion object
phylib_object *phylib_new_vcushion(double x)
{
    phylib_object *obj = (phylib_object *)malloc(sizeof(phylib_object));
    if (obj == NULL)
    {
        return NULL;
    }

    obj->type = PHYLIB_VCUSHION;
    obj->obj.vcushion.x = x;

    return obj;
}

// Create a new table object
phylib_table *phylib_new_table(void)
{
    phylib_table *table = (phylib_table *)malloc(sizeof(phylib_table));
    if (table == NULL)
    {
        return NULL;
    }

    table->time = 0.0;

    // Add cushions and holes to the table
    table->object[0] = phylib_new_hcushion(0.0);
    table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    table->object[2] = phylib_new_vcushion(0.0);
    table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Add holes
    table->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    table->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH});
    table->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    table->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    table->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_WIDTH});
    table->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});

    // Initialize the remaining object pointers to NULL
    for (int j = 10; j < PHYLIB_MAX_OBJECTS; j++)
    {
        table->object[j] = NULL;
    }

    return table;
}

// Copies an object from src to dest
void phylib_copy_object(phylib_object **dest, phylib_object **src)
{
    if (*src == NULL || src == NULL)
    {
        *dest = NULL; // Set dest to NULL if src is NULL
    }
    else
    {
        *dest = (phylib_object *)malloc(sizeof(phylib_object));
        if (*dest != NULL)
        {
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    }
}

// Copies a table from src to dest
phylib_table *phylib_copy_table(phylib_table *table)
{
    phylib_table *new_Table = (phylib_table *)malloc(sizeof(phylib_table));

    if (new_Table == NULL)
    {
        return NULL; // Return NULL if allocation fails
    }

    memcpy(new_Table, table, sizeof(phylib_table));

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            // Allocate memory for a new phylib_object
            phylib_copy_object(&(new_Table->object[i]), &(table->object[i]));
        }
        else
        {
            new_Table->object[i] = NULL;
        }
    }

    return new_Table; // Return the address of the newly allocated phylib_table
}

// Adds an object to the table
void phylib_add_object(phylib_table *table, phylib_object *object)
{
    if (object == NULL || table == NULL)
    {
        return;
    }

    // Find the first NULL slot in the object array and add the object
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }
    }
}

// Frees the memory allocated for the table and its objects
void phylib_free_table(phylib_table *table)
{
    if (table == NULL)
    {
        return;
    }

    // Free each object and then free the table itself
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        free(table->object[i]);
        table->object[i] = NULL;
    }

    free(table);
}

// Subtracts two coordinates
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;
    return result;
}

// Computes the length of a vector
double phylib_length(phylib_coord c)
{
    // Avoid using the exp function for efficiency
    return sqrt(c.x * c.x + c.y * c.y);
}

// Computes the dot product between two vectors
double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    return a.x * b.x + a.y * b.y;
}

// Calculates the distance between two objects
double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{
    if (obj2 == NULL || obj1 == NULL)
    {
        return -1.0; // Invalid input
    }

    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0; // obj1 must be a rolling ball for distance calculation
    }

    double r = PHYLIB_BALL_RADIUS;
    phylib_coord obj1_pos = obj1->obj.rolling_ball.pos;
    phylib_coord obj2_pos;

    switch (obj2->type)
    {
    case PHYLIB_STILL_BALL:
        return phylib_length(phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos)) - (2 * r);

    case PHYLIB_ROLLING_BALL:
        obj2_pos = obj2->obj.rolling_ball.pos;
        return phylib_length(phylib_sub(obj1_pos, obj2_pos)) - (2 * r);

    case PHYLIB_HOLE:
        obj2_pos = obj2->obj.hole.pos;
        return phylib_length(phylib_sub(obj1_pos, obj2_pos)) - PHYLIB_HOLE_RADIUS;

    case PHYLIB_HCUSHION:
        return fabs(obj1_pos.y - obj2->obj.hcushion.y) - r;

    case PHYLIB_VCUSHION:
        return fabs(obj1_pos.x - obj2->obj.vcushion.x) - r;

    default:
        return -1.0; // Invalid obj2 type
        break;
    }
}

void phylib_roll(phylib_object *new, phylib_object *old, double time)
{
    if (old->type != PHYLIB_ROLLING_BALL || new->type != PHYLIB_ROLLING_BALL)
    {
        // Do nothing if not rolling balls
        return;
    }

    // Physics simulation logic
    double time_squared = time * time;

    // Update positions
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x +
                                  old->obj.rolling_ball.vel.x *time +
                                  0.5 * old->obj.rolling_ball.acc.x *time_squared;

    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y +
                                  old->obj.rolling_ball.vel.y *time +
                                  0.5 * old->obj.rolling_ball.acc.y *time_squared;

    // Update velocities
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x *time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y *time;

    // Check for change of sign in velocities
    if ((old->obj.rolling_ball.vel.x * new->obj.rolling_ball.vel.x) < 0)
    {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }

    if ((old->obj.rolling_ball.vel.y * new->obj.rolling_ball.vel.y) < 0)
    {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }
}

unsigned char phylib_stopped(phylib_object *object)
{
    if (object->type != PHYLIB_ROLLING_BALL)
    {
        return 0;
    }

    double speed = sqrt(object->obj.rolling_ball.vel.x * object->obj.rolling_ball.vel.x +
                        object->obj.rolling_ball.vel.y * object->obj.rolling_ball.vel.y);

    if (speed < PHYLIB_VEL_EPSILON)
    {
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.pos = object->obj.rolling_ball.pos;
        object->obj.still_ball.number = object->obj.rolling_ball.number;
        return 1;
    }

    return 0;
}

void phylib_bounce(phylib_object **a, phylib_object **b)
{
    if (*a == NULL || *b == NULL)
    {
        return; // Invalid objects
    }

    // CASE 1: b is a HCUSHION
    if ((*b)->type == PHYLIB_HCUSHION)
    {
        (*a)->obj.rolling_ball.vel.y = -((*a)->obj.rolling_ball.vel.y); // Reverse y-velocity
        (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.acc.y); // Reverse y-acceleration
        return;
    }

    // CASE 2: b is a VCUSION
    if ((*b)->type == PHYLIB_VCUSHION)
    {
        (*a)->obj.rolling_ball.vel.x = -((*a)->obj.rolling_ball.vel.x); // Reverse x-velocity
        (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.acc.x); // Reverse x-acceleration
        return;
    }

    // CASE 3: b is a HOLE
    if ((*b)->type == PHYLIB_HOLE)
    {
        phylib_free_object(*a); // Free memory of a
        *a = NULL;
        return;
    }

    // CASE 4: b is a STILL_BALL
    if ((*b)->type == PHYLIB_STILL_BALL)
    {

        (*b)->type = PHYLIB_ROLLING_BALL;
        (*b)->obj.rolling_ball.pos = ((*b)->obj.still_ball.pos);
        (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.acc.y = 0.0;
        (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = 0.0;
    }

    // CASE 5: b is a ROLLING_BALL
    if ((*b)->type == PHYLIB_ROLLING_BALL)
    {
        phylib_coord r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
        phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
        phylib_coord n = {r_ab.x / phylib_length(r_ab), r_ab.y / phylib_length(r_ab)};
        double v_rel_n = phylib_dot_product(v_rel, n);

        // Update positions
        (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
        (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
        (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
        (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

        // Calculate speeds
        double speed_a = sqrt((*a)->obj.rolling_ball.vel.x * (*a)->obj.rolling_ball.vel.x +
                              (*a)->obj.rolling_ball.vel.y * (*a)->obj.rolling_ball.vel.y);
        double speed_b = sqrt((*b)->obj.rolling_ball.vel.x * (*b)->obj.rolling_ball.vel.x +
                              (*b)->obj.rolling_ball.vel.y * (*b)->obj.rolling_ball.vel.y);

        // Set acceleration based on speed
        if (speed_a > PHYLIB_VEL_EPSILON)
        {
            (*a)->obj.rolling_ball.acc.x = -(((*a)->obj.rolling_ball.vel.x) / speed_a) * PHYLIB_DRAG;
            (*a)->obj.rolling_ball.acc.y = -(((*a)->obj.rolling_ball.vel.y) / speed_a) * PHYLIB_DRAG;
        }

        if (speed_b > PHYLIB_VEL_EPSILON)
        {
            (*b)->obj.rolling_ball.acc.x = -(((*b)->obj.rolling_ball.vel.x) / speed_b) * PHYLIB_DRAG;
            (*b)->obj.rolling_ball.acc.y = -(((*b)->obj.rolling_ball.vel.y) / speed_b) * PHYLIB_DRAG;
        }

        return;
    }
}

unsigned char phylib_rolling(phylib_table *t)
{
    unsigned char rolling_count = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (t->object[i] && t->object[i]->type == PHYLIB_ROLLING_BALL)
        {
            rolling_count++;
        }
    }

    return rolling_count;
}

phylib_table *phylib_segment(phylib_table *table)
{

    if (!phylib_rolling(table))
    {

        return NULL;
    }

    phylib_table *nTable = phylib_copy_table(table);

    double time = PHYLIB_SIM_RATE;
    // do loop to increment time
    while (time <= PHYLIB_MAX_TIME)
    {

        int t = 0;
        while (t < PHYLIB_MAX_OBJECTS)
        {
            if (nTable->object[t] != NULL && nTable->object[t]->type == PHYLIB_ROLLING_BALL)
            {
                phylib_roll(nTable->object[t], table->object[t], time);
            }
            t++;
        }
        int k = 0;
        while (k < PHYLIB_MAX_OBJECTS)
        {
            int i = 0;
            while (i < PHYLIB_MAX_OBJECTS)
            {
                if (i != k && nTable->object[i] != NULL && nTable->object[i]->type == PHYLIB_ROLLING_BALL && nTable->object[k] != NULL)
                {
                    if (phylib_distance(nTable->object[i], nTable->object[k]) < 0.0)
                    {
                        phylib_bounce(&(nTable->object[i]), &(nTable->object[k]));
                        
                        return nTable;
                    }
                }
                i++;
            }

            if (nTable->object[k] != NULL && nTable->object[k]->type == PHYLIB_ROLLING_BALL && phylib_stopped(nTable->object[k]))
            {
                return nTable;
            }
            k++;
        }
        nTable->time += PHYLIB_SIM_RATE; // update time
        time += PHYLIB_SIM_RATE;
    }

    return nTable;
}

// helper function
void phylib_free_object(phylib_object *object)
{
    if (object == NULL)
    {
        return;
    }

    free(object);
}

// Normalizes a vector
phylib_coord phylib_normalize(phylib_coord c)
{
    double len = phylib_length(c);
    phylib_coord result;

    // Avoid division by zero
    if (len != 0.0)
    {
        result.x = c.x / len;
        result.y = c.y / len;
    }
    else
    {
        result.x = 0.0;
        result.y = 0.0;
    }
    return result;
}

// Computes the reflection of a vector against a surface normal
phylib_coord phylib_reflect(phylib_coord v, phylib_coord n)
{
    double dot = phylib_dot_product(v, n);
    phylib_coord r;
    r.x = v.x - 2.0 * dot * n.x;
    r.y = v.y - 2.0 * dot * n.y;
    return r;
}

// Compute the next position of an object based on its current position, velocity, and acceleration
phylib_coord phylib_compute_next_pos(phylib_object *obj)
{
    phylib_coord next_pos;

    // Euler method to compute the next position
    next_pos.x = obj->obj.rolling_ball.pos.x + obj->obj.rolling_ball.vel.x + obj->obj.rolling_ball.acc.x * 0.5;
    next_pos.y = obj->obj.rolling_ball.pos.y + obj->obj.rolling_ball.vel.y + obj->obj.rolling_ball.acc.y * 0.5;

    return next_pos;
}


// Update the table's state based on the elapsed time
void phylib_update_table(phylib_table *table, double elapsed_time)
{
    if (table == NULL || elapsed_time <= 0.0)
    {
        return;
    }

    table->time += elapsed_time;

    // Iterate through each object in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (table->object[i] != NULL)
        {
            phylib_object *obj = table->object[i];

            // Check the type of the object and update accordingly
            switch (obj->type)
            {
            case PHYLIB_STILL_BALL:
                // Still balls do not move, no need to update
                break;
            case PHYLIB_ROLLING_BALL:
            {
                // Update the rolling ball's position based on velocity and acceleration
                phylib_coord next_pos = phylib_compute_next_pos(obj);
                obj->obj.rolling_ball.pos = next_pos;

                // Update velocity based on acceleration
                obj->obj.rolling_ball.vel.x += obj->obj.rolling_ball.acc.x * elapsed_time;
                obj->obj.rolling_ball.vel.y += obj->obj.rolling_ball.acc.y * elapsed_time;
                break;
            }
            case PHYLIB_HOLE:
                // Holes are stationary, no need to update
                break;
            case PHYLIB_HCUSHION:
                // Horizontal cushions are stationary, no need to update
                break;
            case PHYLIB_VCUSHION:
                // Vertical cushions are stationary, no need to update
                break;
            }
        }
    }
}


char *phylib_object_string(phylib_object *object)
{
    static char string[80];
    if (object == NULL)
    {
        snprintf(string, 80, "NULL;");
        return string;
    }
    switch (object->type)
    {
    case PHYLIB_STILL_BALL:
        snprintf(string, 80,
                 "STILL_BALL (%d,%6.1lf,%6.1lf)",
                 object->obj.still_ball.number,
                 object->obj.still_ball.pos.x,
                 object->obj.still_ball.pos.y);
        break;
    case PHYLIB_ROLLING_BALL:
        snprintf(string, 80,
                 "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)",
                 object->obj.rolling_ball.number,
                 object->obj.rolling_ball.pos.x,
                 object->obj.rolling_ball.pos.y,
                 object->obj.rolling_ball.vel.x,
                 object->obj.rolling_ball.vel.y,
                 object->obj.rolling_ball.acc.x,
                 object->obj.rolling_ball.acc.y);
        break;
    case PHYLIB_HOLE:
        snprintf(string, 80,
                 "HOLE (%6.1lf,%6.1lf)",
                 object->obj.hole.pos.x,
                 object->obj.hole.pos.y);
        break;
    case PHYLIB_HCUSHION:
        snprintf(string, 80,
                 "HCUSHION (%6.1lf)",
                 object->obj.hcushion.y);
        break;
    case PHYLIB_VCUSHION:
        snprintf(string, 80,
                 "VCUSHION (%6.1lf)",
                 object->obj.vcushion.x);
        break;
    }
    return string;
}





