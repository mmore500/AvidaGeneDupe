/*
 *  core/Genome.h
 *  avida-core
 *
 *  Created by David Bryson on 3/29/09.
 *  Copyright 2009-2011 Michigan State University. All rights reserved.
 *  http://avida.devosoft.org/
 *
 *
 *  This file is part of Avida.
 *
 *  Avida is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License
 *  as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 *  Avida is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
 *
 *  You should have received a copy of the GNU Lesser General Public License along with Avida.
 *  If not, see <http://www.gnu.org/licenses/>.
 *
 *  Authors: David M. Bryson <david@programerror.com>
 *
 */

#ifndef AvidaCoreGenome_h
#define AvidaCoreGenome_h

#include "apto/platform.h"
#include "avida/core/GeneticRepresentation.h"
#include "avida/core/Properties.h"

#include <typeinfo>
#include <map>


namespace Avida {

  // EpigeneticObject
  // --------------------------------------------------------------------------------------------------------------

  class EpigeneticObject
  {
  public:
    LIB_EXPORT virtual ~EpigeneticObject() = 0;

    LIB_EXPORT virtual bool Serialize(ArchivePtr ar) const = 0;
  };

  // MutationInfo
  struct MutationInfo {
    Apto::String m_name;
    std::vector<int> m_data; // @AML: Should this be a map string:int instead of a vector?

    MutationInfo()=default;
    MutationInfo(
      const Apto::String& name,
      const std::vector<int>& data
    ) :
      m_name(name),
      m_data(data)
    { ; }

    const Apto::String& GetName() const { return m_name; }
    std::vector<int>& GetData() { return m_data; }
    const std::vector<int>& GetData() const { return m_data; }
  };


  // Genome - genetic and epi-genetic heritable information
  // --------------------------------------------------------------------------------------------------------------

  class Genome
  {
  public:
    using mut_infos_t=std::vector<MutationInfo>;
  private:
    class InstSetPropertyMap;

  private:
    HardwareTypeID m_hw_type;
    GeneticRepresentationPtr m_representation;
    Apto::Map<Apto::String, Apto::SmartPtr<EpigeneticObject> > m_epigenetic_objs;

    // std::map<Apto::String, std::vector<int>> m_mut_info;
    std::vector<MutationInfo> m_mut_info;

  public:
    LIB_EXPORT Genome();
    LIB_EXPORT Genome(HardwareTypeID hw, const PropertyMap& props, GeneticRepresentationPtr rep, const mut_infos_t& mut_info=mut_infos_t());
    LIB_EXPORT explicit Genome(const Apto::String& genome_str);
    LIB_EXPORT Genome(const Genome& genome);


    // Accessors
    LIB_EXPORT inline HardwareTypeID HardwareType() const { return m_hw_type; }

    LIB_EXPORT inline PropertyMap& Properties() { assert(m_props.GetSize() > 0); return m_props; }
    LIB_EXPORT inline const PropertyMap& Properties() const { assert(m_props.GetSize() > 0); return m_props; }

    LIB_EXPORT inline GeneticRepresentationPtr Representation() { return m_representation; }
    LIB_EXPORT inline ConstGeneticRepresentationPtr Representation() const { return const_cast<GeneticRepresentationPtr&>(m_representation); }


    // Epigenetic Objects
    template <typename T> bool AttachEpigeneticObject(Apto::SmartPtr<T> obj)
    {
      if (m_epigenetic_objs.Has(T::ObjectKey)) return false;
      m_epigenetic_objs.Set(T::ObjectKey, obj);
      return true;
    }

    template <typename T> Apto::SmartPtr<T> GetEpigeneticObject()
    {
      Apto::SmartPtr<T> rtn;
      rtn.DynamicCastFrom(m_epigenetic_objs.Get(T::ObjectKey));
      return rtn;
    }

    // Mutation information
    mut_infos_t& GetMutInfo() { return m_mut_info; }
    const mut_infos_t& GetMutInfo() const { return m_mut_info; }

    // Conversion
    LIB_EXPORT Apto::String AsString() const;


    // Operations
    LIB_EXPORT bool operator==(const Genome& genome) const;
    LIB_EXPORT Genome& operator=(const Genome& genome);

    LIB_EXPORT bool Serialize(ArchivePtr ar) const;
    LIB_EXPORT static GenomePtr Deserialize(ArchivePtr ar);
    LIB_EXPORT bool LegacySave(void* df) const;

  private:
    class InstSetPropertyMap : public PropertyMap
    {
    private:
      StringProperty m_inst_set;

    public:
      LIB_LOCAL InstSetPropertyMap();
      LIB_LOCAL ~InstSetPropertyMap();

      LIB_LOCAL int GetSize() const;

      LIB_LOCAL bool operator==(const PropertyMap& p) const;

      LIB_LOCAL bool Has(const PropertyID& p_id) const;

      LIB_LOCAL const Property& Get(const PropertyID& p_id) const;

      LIB_LOCAL bool SetValue(const PropertyID& p_id, const Apto::String& prop_value);
      LIB_LOCAL bool SetValue(const PropertyID& p_id, const int prop_value);
      LIB_LOCAL bool SetValue(const PropertyID& p_id, const double prop_value);


      LIB_LOCAL void Define(PropertyPtr p);
      LIB_LOCAL bool Remove(const PropertyID& p_id);

      LIB_LOCAL ConstPropertyIDSetPtr PropertyIDs() const;

      LIB_LOCAL bool Serialize(ArchivePtr ar) const;
    };

  private:
    InstSetPropertyMap m_props;
  };
};

#endif
